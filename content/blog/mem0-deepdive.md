---
title: "Mem0 Deepdive"
date: "2026-08-03"
excerpt: "Mem0 uses an LLM to extract flat, add-only memory (or facts), it uses semantic search to retrieve relevant memory and boosts the ranking by using keyword matching (BM25) and entity matching."
---

## Why do I look at mem0

While I was researching the solutions available in memory space, Mem0 pops up quite a bit, which piques my interest to have a deeper look at it.

Forenote: the v3 implementation is different from its original paper published in 2025

## What is Mem0

A product with memory as product, leveraging lexical search and semantic search to interact with memory. It is not file system based. It has OSS and managed version, with the managed version having more capability than OSS.

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
    1. two independent strings
        1. scope ID + (`agent_id`, `run_id`, `user_id`) -> which gets used as scope key
        2. parsed transcript: `role + content` -> what flows downstream
2. embed the formatted content to retrieve top 10 relevant facts
3. retrieve past 10 original messages in the same session as context
4. send (parsed transcript + last 10 original messages + up to 10 relevant facts + ~34k characters of instruction of fact extraction) to LLM -> gets structured output back, including extracted facts `text` and `attributed_to` (i.e. assistant/user)
    1. based on experiment, this step is the main ‘dedup’ effort
    2. the relevant facts help LLM to decide what extra facts it wants to emit, it is possible that LLM will produce no new facts if the existing facts already cover the gist
    3. 10 original messages are to provide conversational context, this is different from the 10 relevant facts, I got confused here in the first read
5. extracted facts will be encoded in MD5, as a backstop to dedup with the relevant facts
    1. MD5 gets used by exact match, if there is overlap, then skip inserting the fact
    2. survivors get lemmatized by spaCy (for BM25 match in retrieval step)
6. Batch insert
    1. Batch insert all the facts discovered from the one LLM call
    2. Batch insert the fact into SQLite as history (v3 is add only)
7. Entity extraction
    1. spaCy extracts the entities
    2. if normalized string match (lowercased, whitespace-collapsed) with an entity or embedding similarity >= 0.95, route to that row
    3. If entity is new, create a new entity row
    4. append corresponding `memory_id` to `linked_memory_ids` in associated entity
8. Persist the message into the SQLite as context for later
    1. per scope the message is bounded at 10, older messages will get purged

### Failure modes

1. expired twin trap
    1. for an expired fact, though it is not visible upon retrieval, the existence will prevent the same fact to be re-added
    2. some side notes, expiration is user provided at ingestion time, and the field gets used at read time to filter out records. Transition itself is not a thing
2. delete does not erase
    1. asymmetry in records, `delete()` drops the vector row but appends another record in SQLite history as tombstone, marked as `is_deleted=1`, however history reads have no `is_deleted` filter, causing confusion.
    2. only `reset()` will actually erase things: it takes no scope argument, and wipes and drops everything except for entity collection, which creates `linked_memory_ids` corresponds to ghosts

## Retrieval walk through

![Retrieval walk through workflow](/blog/03-retrieval-v3.png)

1. client side initiates the request [sample request]
2. process request
    1. raw query gets embedded
    2. spaCy lemmatizes it + extracts entities
3. semantic search generates candidate pool. Overfetched, `max(60, 4 * top_k)`
4. score boosting
    1. BM25 over `text_lemmatized`, raw score gets smoothed by sigmoid
    2. query entities matched against entity rows, boosts merge by max: the fact gets the stronger of two boosts if matched with two entities
5. score fusion
    1. divisor: sum of active signals’ maxima
    2. threshold: default (0.1) low score does not get evaluated
6. sort and truncate to `top_k`
7. optional reranker (does not change members of candidate list, just change the ranking)
8. for platform version, there is temporal concept (subordinate to semantic), where the temporal intent will first gets classified (without LLM call), and then pass onto a step to rerank the retrieved facts with the time concept
    1. time concept has `time_precision` (day/ week/ month/ year/approximate), with lower precision contributes less into the score while higher precision contributes more
9. return result [sample response goes here]

## Some observations from enterprise use case perspective

1. concurrency
    1. memory creation involves embedding, thinking, inserting
    2. though inserting is atomic, the memory steps as a whole are not atomic
    3. it means that similar messages sent to different instances in a same time window will end up creating duplicates without system noticing it
2. Rollback
    1. no versioning chain
3. version lineage (trace one piece of fact’s evolution)
    1. fact is add only without links
    2. `linked_memory_id` got generated by LLM when extracting facts, but it gets thrown away
    3. history table shows when the fact got added, no other records about the linkage between facts
4. Access control
    1. no object level access control
    2. scope concept is built on `run_id`, `user_id`, `agent_id`. They are filtered fields, not access control, and history table does not even carry a `user_id`
5. Error monitoring
    1. there are failures got silently dropped, such as unconfigured spaCy, which silently loses entity boosting. Vertex -> BM25 no-op (Vertex actually just returns None). pgvector -> planner cliff at scale.
    2. A failed vector insert does not end up in failure, however the fact is still written into history and still gets reported back to the caller as a successful ADD
6. Staleness
    1. no recency or time decay in OSS, so a stale fact may outrank a fresh memory.

## Summary

Mem0 uses an LLM to extract flat, add-only memory (or facts), it uses semantic search to retrieve relevant memory and boosts the ranking by using keyword matching (BM25) and entity matching. In terms of memory itself, the connection between each memory is only implicit, expressed through embedding proximity or a shared entity hub. If the embedding model predates the terms, then split facts about Rubin and Nvidia will just stay unrelated. For enterprise use case, the scalability and correctness and auditability are three big open questions that need to be answered. I think it is hard to find an answer here with Mem0’s flat add-only memory with no explicit link between memory, and time as an afterthought. To continue the search for answers, next blogs will explore Graphiti for temporal knowledge graph and Letta Code for the lineage and memory in a file system.
