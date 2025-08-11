# LLM-Powered Natural-Language Property Search

## Overview

This feature introduces a new endpoint, `/api/search-nl/`, which allows users to search properties using **natural language input**—e.g.,

> "Find 3-bedroom apartments under 2 million DKK near Copenhagen."

When a query is submitted, it is sent to the **Hugging Face Serverless Inference API** (using a lightweight instruction-tuned model). The model’s output is parsed into structured filter parameters that the existing property search logic consumes.

---

## Workflow

| Step | Description |
| ---- | --- |
| 1    | Client sends a free-text query to `POST /api/search-nl/` with JSON payload: `{ "query": "... your question ..." }`. |
| 2    | The Django backend forwards this query to the Hugging Face Inference API using your API token, and receives a response such as: ```{ "bedrooms": 3, "max_price": 2000000, "location": "Copenhagen" }``` |
| 3    | The backend translates this into our existing filter logic—e.g., `.filter(bedrooms=3, price__lte=2000000, city__icontains="Copenhagen")`—and retrieves matching results. |
| 4    | Results are returned as standard JSON property listings to the client (mobile or web). |

---

## Sequence Diagram  
```mermaid
sequenceDiagram
    participant User as User (React Native App)
    participant API as Django API (/search-nl/)
    participant HF as Hugging Face Inference API
    participant DB as Property Database

    User->>API: POST /search-nl/ { query: "3-bedroom under 2M DKK near Copenhagen" }
    API->>HF: Send query to Hugging Face model
    HF-->>API: Parsed filters JSON { bedrooms: 3, max_price: 2000000, location: "Copenhagen" }
    API->>DB: Search properties using filters
    DB-->>API: Matching property listings
    API-->>User: JSON response with property results
````

---

## Requirements

* **Hugging Face API account** (free tier sufficient for low-volume demo usage).
* Django REST Framework for endpoint handling.
* Basic prompt engineering to guide the LLM output into structured JSON.
* Integration with existing property search logic.

---

## Limitations

1. **Response Time** – The endpoint is synchronous; if Hugging Face API latency spikes, user experience may suffer (e.g., 3–10 seconds).
2. **Rate Limits** – Free tier usage from Hugging Face has strict rate limits, which can cause temporary failures if usage is high.
3. **Model Accuracy** – The LLM may occasionally misinterpret queries, leading to incorrect filters or empty results.
4. **Blocking Workers** – In production under synchronous WSGI, long LLM calls block request workers, potentially affecting API throughput under load.

---

## Future Improvements

1. **Async Processing** – Move the Hugging Face call into an async Django view or a Celery background task to prevent blocking.
2. **User Feedback** – Implement a “Searching…” status in the frontend to improve perceived performance.
3. **Caching** – Cache parsed filter results for repeated queries to reduce API calls.
4. **Fine-Tuning** – Fine-tune the LLM or add rule-based post-processing to improve filter extraction accuracy.
5. **Fallback Search** – If Hugging Face fails or times out, fall back to keyword-based search to ensure some results are returned.
