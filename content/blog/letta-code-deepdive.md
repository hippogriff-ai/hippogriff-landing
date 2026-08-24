---
title: "Memory Series Deep Dive: Letta Code's Git-Backed Memory Repo"
date: "2026-08-23"
excerpt: "Letta-code delegates the model to curate the memory folder in the file system, and leverages Git to handle memory progression. Traced with LangSmith: what git actually gets used for, and what replaces it without a shell."
image: "/blog/letta/d1-three-layers.png"
---

## TL;DR

Letta-code delegates the model to curate the memory folder in the file system. Letta-code leverages Git to handle memory progression. One important assumption is that the agent has access to the shell. Git’s worktree allows different actors to make changes and the merge mechanism resolves the divergence. Another benefit Git brings is that provenance and contextual info of the change is preserved in the form of merge history and commit messages.

## Three layers of the past

![Three layers of the past](/blog/letta/d1-three-layers.png)

1. The current context window. It is precious but has limited length.
2. The conversation transcript, which is searchable (hybrid, semantic + keyword) by the agent. Transcript is stored on the disk, append-only. Digging through the transcript is expensive in token cost and takes time, but it provides a good fallback when things are not in context.
3. There is another layer, which is what we will focus on in this post: the model-curated memory in the form of a git-tracked folder. Model can leverage the path and hierarchical structure to organize the memory how it likes.


## Anatomy of memory

1. Memory blocks and external memory.
    1. Memory block is loaded in context and it's short, condensed, high level. Here's the relevant system prompt related to it:

    > Memory blocks are editable segments of the system prompt. Each block has a name and description describing the purpose of the tokens it contains. Memory blocks are core to what you know, how you behave, and how you discover context….Reserve them for durable knowledge that shapes who you are and how you act, plus the indexes that let you discover everything else…Prefer compact indexes and behavioral rules over bulk content — move detail to external memory.

    ![Memory block captured inside an actual LLM request](/blog/letta/memory-block-screenshot.png)
    *Fig: the compiled memory block, byte-for-byte, inside a real request — not documentation, a capture.*

    2. External memory is part of the memory folder but its content does not get loaded into the system prompt. A file tree of the external memory gets loaded and exposed progressively.  Here is how the instruction looks in letta-code’s system prompt:

> **External memory (skills, markdown, & other files)**
>
> External memory is stored outside of the system prompt, including both skills (procedural memory), general-purpose files (markdown files, images, etc.), and shared memory.
>
> - *Skills (procedural memory).* Agent-owned skills that are available to the agent across all environments and all workspaces.
> - *Markdown files.* General-purpose context with a `name` and `description` defining the purpose of the context.
> - *Other files (e.g. reference images).* General-purpose files that are a part of the agent, e.g. reference CSV tables or images.
>
> **Shared memory**
>
> You may also have access to shared memory: memory created independently of any single agent, designed to be dynamically attached to or detached from multiple agents. Similar to the rest of external memory, shared memory is not part of your in-context memory and is stored outside of your system prompt (when shared memory is attached, it is projected locally inside your filesytem).

![External memory arrives as a file tree — names and descriptions only](/blog/letta/skills-tree-crop.png)
*Fig: captured from a real request's system prompt — the skills tree arrives as paths plus one-line descriptions; the content stays on disk until the agent asks for it.*

## Memory lifecycle

### Initialization

Memory repo is initialized automatically based off a boilerplate, with a `system/` folder with default persona file and personal preference file generated. Manual triggering by `/init` is also supported, which will produce richer memory by using your project's git history to infer who you are.

Memory file is in .md format, with frontmatter describing the purpose of the file.

> **[Example — how my Friday dinner preference gets created]**

### Loading
In addition to compiling the `system/` content and the memory file tree into the system prompt, letta-code also instructs the agent on how to use the memory:


> Use **memory** when the change should become part of your future judgment:
> - what you know about the user, projects, workflows, and conventions
> - durable preferences, corrections, and recurring mistakes
> - identity, communication style, and behavioral principles
> - reusable procedures, skills, references, and retrieval paths
>
> …
>
> ## Jogging your memory
> If you come across a reference to something you do not currently have any information about (e.g. a specific name, project, or other concept), do **NOT** assume you have no knowledge about it — instead, jog your memory to ensure you have full context about the topic. This includes:
> - Recalling past conversations
> - Searching through MemFS (running `grep` or other search operations)
> - Using any other available search tools

### Updating

![The memory edit pipeline](/blog/letta/d2-edit-pipeline.png)

There are two sources of memory evolution: main agent and dream agent.
Main agent writes the durable insights down as the memory in band while doing a task for the user
[original system prompt link]:

> - *System prompt learning.* … When you discover a durable insight — a corrected assumption, a user preference, a pattern in your mistakes… Updates should generalize across situations rather than simply recording individual events; the goal is to make your future self act better, not just remember more.

**How to change the memory?**

According to the system prompt there are two ways:

1. The memory tool shorthand
2. Direct file edits (the full control)

> There are two ways to change memory:
>
> - **The `memory` tool (shorthand).** Use it for small, targeted edits. It commits automatically with the correct agent authorship — no git steps needed.
> - **Direct file edits (full control).** For larger changes — restructuring directories, rewriting several blocks — edit the projected files directly, then commit…

Some additional instructions on how memory should look like:
> *Keep blocks lean.* Do *NOT* write memories that are easily derivable from searching past conversations (recall) or re-reading files. Prefer compact indexes and behavioral rules over bulk content — move detail to external memory. The harness flags your system prompt for `/doctor` when it grows too large.
>
>…
>
> Memory markdown files must start with YAML frontmatter containing a non-empty `description:` field. The `memory` and `memory_apply_patch` tools add and preserve this automatically; when using raw file edits, preserve existing frontmatter or add it before committing. The MemFS pre-commit hook enforces this requirement, rejects unknown keys, and prevents changes to protected `read_only` files. Skill `SKILL.md` files use their own skill frontmatter format.

### What happens after commit

Before every model call, letta-code will compare the cached memfs revision to the current HEAD's revision. If they match, then reuse the cache (0.04s walltime in screenshot). If not, then recompile (0.41s).

![Cache hit: 0.04s, cached true, pre-merge revision](/blog/letta/integrator-resolve-cache-hit.png)
*Fig: cache hit (0.04s), `cached: true`, revision `5feafb0…`, 19,757 chars.*

![Cache miss after the merge: 0.41s, cached false, new revision](/blog/letta/integrator-resolve-cache-hit-miss.png)
*Fig: after the merge lands, the same check misses (0.41s), `cached: false`, revision `8bf0c09…` (the merge commit), prompt 58 chars heavier.*

## The second memory writer: Dream agent

**What is dream agent**

Dream agent is an out-of-band agent that reads the transcript of the conversations and the existing memory to propose changes or corrections to the memory itself.

**How does it work:**

![Dream waterfall — reply at 3.2s, dreaming until ~50s](/blog/letta/dream-waterfall-screenshot.png)
*Fig: Dreaming is non-blocking: user gets response at 3.2s, the rest pipeline ran afterwards. Right pane: the dreamer's own system prompt.*

![How a dream ends](/blog/letta/d3-dream-outcomes.png)

1. Input of the dream is current memory + the new transcripts after the mark left by the last dreaming. After a successful dream, harness will advance the cursor to the last transcript row, so that the next dream will pick up from where the last dream ended. If a dream fails, harness will not move the cursor.

2. When does the dreaming happen? The dream can be fired in different ways:
    * Step-count threshold (the default).
    * Upon the compaction, which is a logically good pause point to really reflect and modify the memory.
    * It could also be triggered explicitly by the user.

3. What if there's a conflict? Here is the magic of Git again. Dream Agent will leverage the worktree to work on a copy of the memory. Once it's done it will try to merge into the parent branch and that will kick off the Git mechanism which I will talk about in the next section.


**What can dream agent change:**

According to the system prompt:
> You can make two kinds of updates:
> 1. **Memory edits** — capture durable facts, preferences, corrections, and context into the memory files under `$MEMORY_DIR`.
> 2. **Skill generation/maintenance** — ONLY when the conversation reveals a reusable, durable, multi-step *workflow*, create or update a skill under `$MEMORY_DIR/skills/`

## Git in memory curation
Now the highlight: Git.

Starts with why: Memory has two writers: main agent (in-band) and dream agent (out of band). It needs a mechanism to prevent two writers from interfering with each other.

Git helps with this in three areas:

1. Worktree: isolation. The dream agent gets its own branch. Main agent keeps writing while dream agent does the work.
2. Merge: reconciliation. Dream agent's proposal comes back via merging. If the parent HEAD moved (because of main agent's editing), conflicts get resolved before the merge lands. Details in the next part.
3. Commit: atomicity. Every change from either writer lands as one commit.

![The explicit merge flow](/blog/letta/d4-explicit-merge.png)

There are two merge modes:
* Merge auto, which is quite straightforward: if there's no merge conflict, go ahead. If there's a conflict, abort and discard the pending changes. The later dream will retry from scratch.
* Merge explicit, which will require a spawn of the main agent to resolve the conflicts. It starts by merging the current HEAD of parent branch into working branch if the parent moved, then reason through the difference and try to merge the branch back to parent.

Let's run through an example of the dream finalization phase:

When merge mode is explicit and dream actually proposed something, integrator will be triggered:
![The integrator's entire input](/blog/letta/integrator-prompt-five-params.png)
*Fig: the integrator's full input contract: worktree, repo, one branch by name, a pinned base commit, the dream's ID. Scope arrives as parameters; nothing is discovered.*

Then the proposal gets fed into the model as git diff:
![The proposal arrives as a git diff](/blog/letta/integrator-round1-diff-output.png)
*Fig: round 1 — one combined shell call; the dreamer's proposal arrives as a diff against the pinned base. Note the stat line: the whole divergence is 1 insertion, 1 deletion.*

Afterwards, merge policy kicked in.
![The merge policy visibly executing](/blog/letta/integrator-refine-edit.png)
*Fig: the refine — old_string is the dreamer's run-on proposal; new_string is the integrator's rewrite under the user's 40-word merge policy.*

After memory merge was done, agent's prompt gets recompiled.
![The agent's own prompt recompiles with the memory it just merged](/blog/letta/integrator-memfs-revision-flip.png)
*Fig: after its own `git merge`, the integrator's next prompt compile picks up revision `8bf0c09` — the commit it just created.*


## A bit more on git: provenance

In the first few traces I saw `git diff`, but not `git history`, which makes me wonder if it is used at all. To test it, I planted two facts whose origins live only in `git history`. I edited the memory file directly and committed, with no conversation behind either change:
- Ben is now pescatarian, and the reason (his doctor flagged a B12 deficiency) exists only in the commit message.
- Tomás joined the crew the same way, never mentioned in any chat.

The facts themselves sit in memory, so the agent knows them. But the answers to when and why live only in git history.


> “A provenance question about your memory of my dinner crew: why did Ben switch from vegetarian to pescatarian, and when did that enter your memory? And how did you first learn about Tomás — I don't remember ever telling you about him in a conversation. Show me exactly how you know.”

![Provenance turn — the agent delegates the archaeology](/blog/letta/provenance-waterfall.png)

The agent first spawned a subagent to do the digging. The subagent started by grepping the memory folder for the two names. The matches included files inside `.git` (`.git/logs/HEAD`, `COMMIT_EDITMSG`), where commit messages sit as plain text.
![First move: grep sweeps the memory folder and hits git's own internals](/blog/letta/provenance-grep-reflog.png)

Then `git log` for the full history: three authors, dated, with messages.
![The full three-author history in one tool output](/blog/letta/provenance-git-log.png)

The answer:
![The answer, with commit and diff quoted](/blog/letta/provenance-final-answer.png)
*Fig: "I do not have evidence that you told me about Tomás in a normal conversation."*

## Is Git absolutely needed?

Git is great, but it needs shell access to actually unleash the power, otherwise mimicking a git-like surface sounds like a heavy lift and error prone.

Let's take a step back on how Git is actually being used in here.

![Git's jobs and their shell-free replacements](/blog/letta/d5-git-replacements.png)

1. Git commit: atomic change
2. git diff: rich context for divergence resolution
3. git log: provenance
4. git status --porcelain: short-circuit when the memory repo has uncommitted changes

Here I listed diff and log as separate rows, because I observed `git diff` alone in conflict resolution. Git history came up only for provenance questions (please correct me if this view is too limited).

Ok, so can we find an alternative achieving the similar goals?

1. Atomic change: a DB that supports transactions can get this covered
2. Divergence: Retain the versions themselves by using content SHA, and any two can be diffed.
3. Provenance: the tricky one. Discussion below.
4. Uncommitted change check: compare and swap and content SHA comparison.

Provenance is tricky because plain file tools have no slot for the "why". Instead of building a custom tool to record the reason, we can lean on implicit linkage: record a session ID and message ID with each write. The why then lives in the transcript those IDs point to. Less direct than a commit message. Conceptually it works.


## Summary

Letta-code's answer to agent memory: model-driven & git-backed memory folder. It unleashes the power of the model to let it write what it thinks will help its future self, while confining every change within `git`, so each one is traceable. However it needs shell access, which makes it hard for a lot of server-side harnesses to adopt out of the box for security reasons unless sandbox is already part of the infrastructure. Good news: we can use CAS and a relational database to get similar benefits.

One takeaway: Use `git` when the agent has access to shell. Use `CAS + a relational store + reinvent a way to replace commit message` when it does not.
