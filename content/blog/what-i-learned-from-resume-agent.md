---
title: "What I learned from building a resume agent"
date: "2026-02-08"
excerpt: "Finishing an unfinished business, sharing some learnings on agent design"
pinned: true
---
## Why I built this resume agent (Talent Promo)
I always feel defeated when revising my resume. The mixed feeling of "I have so much to offer" and "I am not enough" keeps fighting each other. And guess what, my friends do not enjoy the process either.

About a year ago, two other friends and I tried to build a resume agent in a Google Agent SDK hackathon. We abandoned it halfway because of scheduling and other challenges. I really wanted to materialize the vision, therefore started to tinker on it in spare time off and on. Yeah, it took a while, multiple redesigns from agent harness all the way to UX. And today, it is finally in a not-so-unusable state.

## Things I learned
### Workflow or agentic
I chose the workflow design because an orchestrated stage made most sense to me as a user:
Research target and gaps -> Discover hidden power -> Initial Draft -> Iteration Drafting -> Final output

Meanwhile, I keep doubting myself if this is the best way. [Bitter lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html), and this [article](https://x.com/buckeyevn/status/2014171253045960803?s=46) from Minh Pham mentioned using a human way of thinking to solve problems may restrict the power of LLM. I might go do some experimentation on different agent architectures.

The two architectures on my target list are:
- main-subagents for efficient context management
- skill-based single agent architecture: I do notice that there is a lot of shareable context throughout the workflow. As a matter of fact, I am passing the state along the current orchestrated agent architecture.

### Agentic runtime
I am a fan of `langgraph`. The flexibility to define state, control the state flow, and native support of human-in-the-loop thanks to checkpointing has expanded the canvas greatly to build an agent.
`deepagents` has also been on my radar. I like it a lot for agent harness without tying to a specific model provider. Though I did not use `deepagents` lib in this project, I want to thank it for teaching me how to think of virtual file system vs. database retrieval. I am amazed at the duck typing that bridged the strong Linux command skill from LLM and RDBMS retrieval.


### Development-time eval harness to allow coding agent to better help
If I had enough resources: curate a set of example inputs and outputs, get a comparator to watch the actual output vs expected output. The comparator can be a function if there is a definitive aspect of the criteria, otherwise an LLM judge that shares an expert's taste. Human will drive the cycle, trigger a batch run, get comparison, after analyzing failure modes, update the prompt (or LLM judge), keep going.

However, for a hobby project, I need to find some shortcut. Inspired by the famous [ralph loop](https://ghuntley.com/loop/), if you can give clear criteria for the coding agent, most likely it will get it for you EVENTUALLY.
Here is what I did:
- Acquired a deep research report on what a good resume should look like
- Fed that into Claude Code, asking for a draft of grader agent that uses scoring rubric (I had some luck with the scoring rubric idea, got some good results in a [finetuning LLM](https://www.youtube.com/watch?v=dleo77BuB1w) for wine tasting note generation project)
- Test drove the judge on a handful of examples (the draft, the job posting, and the
  original resume)
- Set up eval harness whose output went directly to the repo
- Gave ralph loop instruction: tune the drafting prompt, ensure score from LLM judge needs to be above 88. Then let the ralph do whatever it thinks it should do to reach there (except for changing the judge, it needs my permission to do so if it really thinks judge should change).

The drafting agent started to behave a lot better than before, but is it there already? Not yet, but it can sometimes generate something I did not think of.

### Memory
Well well well, I wanted to build it very much! Stay tuned! I am trying to integrate it with another fun project. In this resume project, I got hesitant because of the PII, therefore I removed all the persistence.
Btw, inspired by some tweets, I added `CONTINUITY.md` as an external memory for the coding agent to know what I have asked it to do. I find it quite helpful even for myself — when vibe coding on a project on and off, it is so easy to lose track of where things are.

