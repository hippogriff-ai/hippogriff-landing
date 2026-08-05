---
title: "Agent Memory Series: Mem0 Deepdive"
date: "2026-08-05"
excerpt: "Mem0 uses an LLM to extract flat, add-only memory (or facts), and it uses semantic search to retrieve relevant memory and boosts the ranking by using keyword matching (BM25) and entity matching."
---

## Why do I look at Mem0

While I was researching the solutions available in the memory space, Mem0 pops up quite a bit, which piques my interest to have a deeper look at it.

Forenote: the v3 implementation is different from its [original paper](https://arxiv.org/abs/2504.19413) published in 2025.

## What is Mem0

Mem0 is a memory layer for agentic apps, leveraging an LLM to extract facts from the transcript, and search the facts back to serve as memory. It keeps the derived facts, not the transcripts. It is not file system based. It has an [OSS](https://github.com/mem0ai/mem0) and a managed version, with the managed version having more capability than OSS.

## Components in Mem0

![Mem0 components high level flow chart](/blog/01-components-v4.png)

- Core components
    - LLM (responsible for extracting facts from user and assistant input as candidates for later storage)
    - Embedding model

        It powers the novelty reference retrieval at insert time and candidate retrieval at search time.
    - Fusion logic

        It exists in the form of code, and scores the semantically retrieved candidates with BM25/ entity signals. Worth noting that the semantically retrieved pool is the starting point: a candidate with perfect keyword matching but outside of the pool does not get evaluated.
    - Storage
        - Qdrant

            It stores two types of vectors: one for facts, the other for entity hubs with `linked_memory_ids`.
        - SQLite

            It saves two types of records: A. rolling raw messages, which will be used as context to extract facts, and B. history of added facts.
- Optional components
    - Reranker

        It gets used AFTER the candidates are retrieved, instead of saving those candidates that got excluded in semantic search.
    - spaCy

        It has two jobs: A. extracts the entities that populate the entity store, and B. lemmatizes facts to produce keywords for BM25. Therefore, if spaCy is not installed, entity boosting will not exist, and lemmatization falls back to raw text, which silently degrades the quality without raising errors.
    - fastembed (Qdrant only)

        It produces sparse vectors for BM25.
    - Other vector stores

        Mem0 provides generic interfaces that can integrate with 20+ providers, including pgvector, chroma, Qdrant (default), however the capabilities are different, depending on the actual provider.

## Ingestion walk through

![Ingestion walk through: restaurant booking example](/blog/02-ingestion-v4.png)

There are 8 steps involved in ingestion:

1. Produce the inputs

    Let's say an agent and I just had a conversation about an upcoming dinner plan. The conversation covers me wanting to book a table at Nobu, a dietary restriction, and the agent's recommendation based on that restriction. Then the conversation gets sent to Mem0 to generate memory. The scope is `user_id="vicki", run_id="dinner", agent_id="resto_assistant"` and each entry in the transcript gets parsed as `role + content` (e.g. `user + wants to book a table at Nobu`, `assistant + recommends black cod miso`).

2. Embed the parsed transcript to retrieve the top 10 relevant facts

    If there are existing memories about restaurant booking, those facts surface here as the novelty reference so that the LLM does not regenerate overlapping facts later on.

3. Retrieve the past 10 original messages in the same session as context

4. Send to LLM

    Send everything mentioned in previous steps (parsed transcript + last 10 original messages + up to 10 relevant facts + ~34k characters of fact-extraction instructions) to the LLM -> gets structured output back, including extracted facts `text` and `attributed_to` (i.e. assistant/user).

    For the dinner transcript, three facts get extracted: the booking, the allergy and the recommendation. I did not realize the dedup functionality of the LLM until I asked the coding agent to ingest a similar transcript again: the LLM call was fired, but no new facts extracted, and some later steps short-circuited. I am glad I saw this case, but want to bring up that LLM dedup is an intent: it will still generate facts [when in doubt](https://github.com/mem0ai/mem0/blob/50bdaaea/mem0/configs/prompts.py#L578).

    One more thing: there are two 10s: the 10 original messages (as context) and the 10 relevant facts (as novelty reference). I got confused on my first read.

5. Extracted facts will be encoded in MD5, as a backstop to dedup with the relevant facts

    MD5 gets used by exact match: if there is overlap, the fact gets skipped. Afterwards, survivors get lemmatized by spaCy (for BM25 matching in the retrieval step).

6. Batch insert

    Insert all the facts discovered from the one LLM call into the vector DB. Meanwhile, insert the facts into SQLite as history (v3 is add only).

7. Entity extraction

    spaCy extracts the entities. The extracted entity will go through a create-or-update process: if a normalized string match (lowercased, whitespace-collapsed) or embedding similarity >= 0.95 hits an existing entity, use that row; if the entity is new, create a new entity row. Then, append the fact's `memory_id` to `linked_memory_ids` in the entity row.

8. Persist the message into SQLite as context for later

    Store the message in SQLite. Because messages are bounded at 10 per scope, older messages will get purged.

### Failure modes

- Expired twin trap

    For an expired fact, though it is not visible upon retrieval, the existence will prevent the same fact from being re-added. You might wonder where the expiration comes from. It is user provided at ingestion time, and the field gets used at read time to filter out records. Transition itself is not a thing.

- Delete does not erase

    There is asymmetry in records: `delete()` drops the vector row but appends another record in SQLite history as a tombstone, marked as `is_deleted=1`. However, history reads have no `is_deleted` filter, causing confusion about whether the retrieved history is deleted or not.

    From the code, it seems that only `reset()` will actually erase things: it takes no scope argument, and wipes and drops everything **except** for the entity collection, which leaves the `linked_memory_ids` stored within an entity pointing to ghosts.

## Retrieval walk through

![Retrieval walk through workflow](/blog/03-retrieval-v4.png)

1. Client side initiates the request

    Real call against mem0ai 2.0.15, OSS, embedded Qdrant, text-embedding-3-small.

    ```python
    from mem0 import Memory

    m = Memory()   # embedded Qdrant at /tmp/qdrant, SQLite at ~/.mem0/history.db

    results = m.search(
        "What should I order at Nobu on Saturday?",
        filters={"user_id": "vicki", "run_id": "dinner"},  # v3: ids live INSIDE filters
        top_k=5,          # step 3 still fetches max(60, 4 x top_k) = 60
        threshold=0.1,    # step 5 — gates the raw semantic score, before any boost
        explain=True,     # adds score_details, which is what makes steps 4-5 visible
    )
    ```

    Two things in there: in v3 the identity fields moved inside `filters` (a top-level `user_id=` now raises), and `top_k=5` is not the fetch size: the store is asked for 60.

2. Process request

    The raw query gets embedded. spaCy lemmatizes it and extracts "Nobu" as a query entity.

3. Semantic search generates the candidate pool

    Overfetched: `max(60, 4 * top_k)`, therefore we end up with 60 here. This step decides who enters the candidate pool.

4. Score boosting

    BM25 over `text_lemmatized`. The raw score is unbounded, so a sigmoid gets applied to normalize it into [0,1] before fusion. The sigmoid's parameters are also calibrated by query length, so that long queries don't inflate the signal. Query entities get matched against entity rows. One detail caught my attention: instead of adding boosts up, it actually merges by max, so the fact gets the stronger of two boosts if matched with two entities.

5. Score fusion

    There is a threshold (default 0.1) that filters out facts with a low semantic score before the fusion. Survivors will have their three signals added up, then divided by the sum of the active signals’ maxima (1.0 semantic + 1.0 BM25 + 0.5 entity, so 2.5 when all three are on).

6. Sort and truncate to `top_k`

7. Optional reranker

    This step does not change the membership of the candidate list; it just changes the ranking.

8. [Temporal concept](https://mem0.ai/blog/introducing-temporal-reasoning-in-mem0) (platform only)

    It is subordinate to semantic: the temporal intent will first get classified (without an LLM call), and then get passed on to a step to rerank the retrieved facts with the temporal concept.

    The temporal concept has `time_precision` (day / week / month / year / approximate): lower precision contributes less to the score while higher precision contributes more.

9. Return result

    Watch the second result: the allergy fact scores 0.096, with no BM25 hit and no entity match, yet it gets divided by the same 2.5 as the row that matched both.

    ```json
    {
      "results": [
        {
          "id": "cef9e18d-...",
          "memory": "Assistant recommended Nobu's black cod miso as the signature dish to order.",
          "score": 0.7362,
          "user_id": "vicki",
          "run_id": "dinner",
          "attributed_to": "assistant",
          "created_at": "2026-08-03T03:41:12.884Z",
          "score_details": {                  // only present because explain=True
            "semantic_score":     0.6447,     // step 3
            "bm25_score":         0.6977,     // step 4, sigmoid-normalized from raw 6.1945
            "entity_boost":       0.4980,     // step 4, "Nobu" at sim 1.0, damped for 3 links
            "raw_score":          1.8404,     // 0.6447 + 0.6977 + 0.4980
            "max_possible_score": 2.5,        // step 5 — 1.0 + 1.0 (any BM25) + 0.5 (any entity)
            "final_score":        0.7362,     // 1.8404 / 2.5
            "threshold":          0.1
          }
        },
        {
          "id": "c78f4d4c-...",
          "memory": "User is allergic to shellfish and must avoid oysters and shrimp.",
          "score": 0.0960,
          "score_details": { "semantic_score": 0.2401, "bm25_score": 0.0,
                             "entity_boost": 0.0, "max_possible_score": 2.5 }
        }
      ]
    }
    ```

## Some observations from enterprise use case perspective

- Concurrency

    Memory creation involves embedding, thinking, inserting. Though inserting is atomic, the memory steps as a whole are not atomic. It means that similar messages sent to different instances in the same time window will end up creating duplicates without the system noticing it.

- Rollback

    No versioning chain.

- Version lineage of a fact

    Facts are add only without links. `linked_memory_ids` got generated by the LLM when extracting facts, but they get thrown away later on. The history table shows when the fact got added; there are no other records about the linkage between facts.

- Access control

    No object level access control. The scope concept is built on `run_id`, `user_id`, `agent_id`. They are filtered fields, not access control, and the history table does not even carry a `user_id`.

- Error monitoring

    There are failures that get silently dropped, such as unconfigured spaCy, which loses entity boosting. For Vertex, BM25 is a no-op: it actually just returns None. For pgvector, some articles report a planner cliff at scale.

    A failed vector insert for a fact does not end up in failure: the fact is still written into history and still gets reported back to the caller as a successful ADD.

- Staleness

    No recency or time decay in OSS, so a stale fact may outrank a fresh memory.

## Summary

Mem0 uses an LLM to extract flat, add-only memory (or facts), and it uses semantic search to retrieve relevant memory and boosts the ranking by using keyword matching (BM25) and entity matching. 

In terms of memory itself, the connection between each memory is only implicit, expressed through embedding proximity or a shared entity hub. If the embedding model predates the terms, then split facts about Rubin and Nvidia will just stay unrelated. 

For the enterprise use case, scalability, correctness, and auditability are three big open questions that need to be answered. I think it is hard to find an answer here with Mem0’s flat add-only memory with no explicit link between memories, and time as an afterthought. 

To continue the search for answers, next blogs will explore Graphiti for temporal knowledge graph and Letta Code for the lineage and agent-managed memory in a file system.
