---
title: "Mem0 Deepdive"
date: "2026-08-03"
excerpt: "Mem0 uses an LLM to extract flat, add-only memory (or facts), it uses semantic search to retrieve relevant memory and boosts the ranking by using keyword matching (BM25) and entity matching."
---

## Why do I look at Mem0

While I was researching the solutions available in memory space, Mem0 pops up quite a bit, which piques my interest to have a deeper look at it.

Forenote: the v3 implementation is different from its [original paper](https://arxiv.org/abs/2504.19413) published in 2025

## What is Mem0

Mem0 is a memory layer for agentic apps, leveraging LLM to extract facts from transcript, and search the facts back to serve as memory. It keeps the derived facts, not the transcripts. It is not file system based. It has [OSS](https://github.com/mem0ai/mem0) and managed version, with the managed version having more capability than OSS.

## Components in Mem0

![Mem0 components high level flow chart](/blog/01-components-v3.png)

- Core components
    - LLM (responsible to extract facts from user and assistant input as candidate for later storage)
    - embedding model
        - powers the novelty reference retrieval at insert time and candidates retrieval at search time
    - fusion logic
        - code, scores the semantically retrieved candidates with BM25/ entity signals
            - semantically retrieved pool is the starting point, a candidate with perfect keyword matching but outside of the pool does not get evaluated
    - Storage
        - Qdrant
            - for facts stored as vector
            - for entity hubs + `linked_memory_ids` stored as vector
        - SQLlite
            - rolling raw messages, which will be used as context to extract facts
            - history of added facts
- Optional components
    - reranker
        - it gets used AFTER the candidates are retrieved, instead of saving those candidates that got excluded in semantic search
    - spaCy
        - two jobs:
            - extracts the entities that populate the entity store
            - lemmatizes facts to prodce keywords for BM25
        - if not installed, entity boosting will not exist, and lemmatization falls back to raw text, which silently degrades the quality without raising errors
    - fastembed (Qdrant only)
        - produce sparse vector for BM25
    - other vector stores
        - Mem0 provides generic interfaces that can integrate with 20+ providers, including pgvector, chroma, qdrant (default), however the capabilities are different, depends on the actual provider.

## Ingestion walk through

![Ingestion walk through: restaurant booking example](/blog/02-ingestion-v3.png)

There are 8 steps involved in ingestion:

1. produce the inputs
    - two independent strings
        - scope ID + (`agent_id`, `run_id`, `user_id`) -> which gets used as scope key
        - parsed transcript: `role + content` -> what flows downstream
2. embed the formatted content to retrieve top 10 relevant facts
3. retrieve past 10 original messages in the same session as context
4. send (parsed transcript + last 10 original messages + up to 10 relevant facts + ~34k characters of instruction of fact extraction) to LLM -> gets structured output back, including extracted facts `text` and `attributed_to` (i.e. assistant/user)
    - based on experiment, this step is the main ‘dedup’ effort
    - the relevant facts help LLM to decide what extra facts it wants to emit, it is possible that LLM will produce no new facts if the existing facts already cover the gist
    - 10 original messages are to provide conversational context, this is different from the 10 relevant facts, I got confused here in the first read
5. extracted facts will be encoded in MD5, as a backstop to dedup with the relevant facts
    - MD5 gets used by exact match, if there is overlap, then skip inserting the fact
    - survivors get lemmatized by spaCy (for BM25 match in retrieval step)
6. Batch insert
    - Batch insert all the facts discovered from the one LLM call
    - Batch insert the fact into SQLite as history (v3 is add only)
7. Entity extraction
    - spaCy extracts the entities
    - if normalized string match (lowercased, whitespace-collapsed) with an entity or embedding similarity >= 0.95, route to that row
    - If entity is new, create a new entity row
    - append corresponding `memory_id` to `linked_memory_ids` in associated entity
8. Persist the message into the SQLite as context for later
    - per scope the message is bounded at 10, older messages will get purged

### Failure modes

- expired twin trap
    - for an expired fact, though it is not visible upon retrieval, the existence will prevent the same fact to be re-added
    - some side notes, expiration is user provided at ingestion time, and the field gets used at read time to filter out records. Transition itself is not a thing
- delete does not erase
    - asymmetry in records, `delete()` drops the vector row but appends another record in SQLite history as tombstone, marked as `is_deleted=1`, however history reads have no `is_deleted` filter, causing confusion.
    - only `reset()` will actually erase things: it takes no scope argument, and wipes and drops everything except for entity collection, which creates `linked_memory_ids` corresponds to ghosts

## Retrieval walk through

![Retrieval walk through workflow](/blog/03-retrieval-v3.png)

1. client side initiates the request

    Real call against mem0ai 2.0.15, OSS, embedded Qdrant, text-embedding-3-small.

    ```python
    from mem0 import Memory

    m = Memory()   # embedded Qdrant at /tmp/qdrant, SQLite at ~/.mem0/history.db

    results = m.search(
        "What should I order at Nobu on Saturday?",
        filters={"user_id": "vicki", "run_id": "dinner"},  # v3: ids live INSIDE filters
        top_k=5,          # step 3 still fetches max(60, 4 x top_k) = 60
        threshold=0.1,    # step 5.2 — gates the raw semantic score, before any boost
        explain=True,     # adds score_details, which is what makes steps 4-5 visible
    )
    ```

    Two things in there: in v3 the identity fields moved inside `filters` (a top-level `user_id=` now raises), and `top_k=5` is not the fetch size: the store is asked for 60.

2. process request
    - raw query gets embedded
    - spaCy lemmatizes it + extracts entities
3. semantic search generates candidate pool. Overfetched, `max(60, 4 * top_k)`
4. score boosting
    - BM25 over `text_lemmatized`, raw score gets smoothed by sigmoid
    - query entities matched against entity rows, boosts merge by max: the fact gets the stronger of two boosts if matched with two entities
5. score fusion
    - divisor: sum of active signals’ maxima
    - threshold: default (0.1) low score does not get evaluated
6. sort and truncate to `top_k`
7. optional reranker (does not change members of candidate list, just change the ranking)
8. for platform version, there is [temporal concept](https://mem0.ai/blog/introducing-temporal-reasoning-in-mem0) (subordinate to semantic), where the temporal intent will first gets classified (without LLM call), and then pass onto a step to rerank the retrieved facts with the time concept
    - time concept has `time_precision` (day/ week/ month/ year/approximate), with lower precision contributes less into the score while higher precision contributes more
9. return result

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
            "bm25_score":         0.6977,     // step 4.1, sigmoid-normalized from raw 6.1945
            "entity_boost":       0.4980,     // step 4.2, "Nobu" at sim 1.0, damped for 3 links
            "raw_score":          1.8404,     // 0.6447 + 0.6977 + 0.4980
            "max_possible_score": 2.5,        // step 5.1 — 1.0 + 1.0 (any BM25) + 0.5 (any entity)
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

- concurrency
    - memory creation involves embedding, thinking, inserting
    - though inserting is atomic, the memory steps as a whole are not atomic
    - it means that similar messages sent to different instances in a same time window will end up creating duplicates without system noticing it
- Rollback
    - no versioning chain
- version lineage (trace one piece of fact’s evolution)
    - fact is add only without links
    - `linked_memory_id` got generated by LLM when extracting facts, but it gets thrown away
    - history table shows when the fact got added, no other records about the linkage between facts
- Access control
    - no object level access control
    - scope concept is built on `run_id`, `user_id`, `agent_id`. They are filtered fields, not access control, and history table does not even carry a `user_id`
- Error monitoring
    - there are failures got silently dropped, such as unconfigured spaCy, which silently loses entity boosting. Vertex -> BM25 no-op (Vertex actually just returns None). pgvector -> planner cliff at scale.
    - A failed vector insert does not end up in failure, however the fact is still written into history and still gets reported back to the caller as a successful ADD
- Staleness
    - no recency or time decay in OSS, so a stale fact may outrank a fresh memory.

## Summary

Mem0 uses an LLM to extract flat, add-only memory (or facts), it uses semantic search to retrieve relevant memory and boosts the ranking by using keyword matching (BM25) and entity matching. In terms of memory itself, the connection between each memory is only implicit, expressed through embedding proximity or a shared entity hub. If the embedding model predates the terms, then split facts about Rubin and Nvidia will just stay unrelated. For enterprise use case, the scalability and correctness and auditability are three big open questions that need to be answered. I think it is hard to find an answer here with Mem0’s flat add-only memory with no explicit link between memory, and time as an afterthought. To continue the search for answers, next blogs will explore Graphiti for temporal knowledge graph and Letta Code for the lineage and memory in a file system.
