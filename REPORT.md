# AI Support Agent Evaluation & Failure Analysis Report

## 1. Why Headline Metrics are Misleading
Aggregate metric scores (such as overall accuracy or semantic similarity) obscure critical failure modes in real-world customer support:
* **Format vs. Substance:** Standard NLP similarity metrics reward polite, nicely formatted responses even if the underlying technical steps provided are incorrect or hallucinated.
* **Averaging Out Edge Cases:** An aggregate 90% accuracy score sounds strong, but if the uncaptured 10% represents legal threats, out-of-scope demands, or billing disputes, the operational risk is high.
* **Blindness to Tone Escalation:** Standard keyword matching fails to evaluate whether an agent effectively de-escalates frustrated customers or exacerbates their issues.

## 2. Failure Analysis & Dataset Limitations
* **Retrieval Boundary Bottleneck:** When user queries lack exact keywords matching the knowledge base, dense vector retrieval can surface partially relevant context, causing the agent to hallucinate incorrect resolutions.
* **Single-Turn Limitation:** Real support channels require managing conversation context across multi-turn interactions, whereas single-turn pipelines miss evolving user context.
* **Historical Policy Noise:** Customer support datasets often contain conflicting resolutions due to internal policy updates over time.

## 3. Decision Log (10 Non-Obvious Engineering Decisions)
1. **Model Choice:** Selected `gpt-4o-mini` for both generation and evaluation due to strict JSON output handling and balanced latency.
2. **Context Formatting:** Formatted Knowledge Base context with explicit field markers (`Issue:`, `Solution:`) to prevent context bleeding across entries.
3. **Low Temperature Setting (`0.2`):** Set generation temperature low to prioritize retrieval accuracy over creative phrasing.
4. **Programmatic LLM-as-a-Judge:** Used structured JSON schema forcing numerical scoring (0–10) and explicit hallucination flags for clear evaluation metrics.
5. **Deterministic Evaluator (`0.0` Temp):** Configured the evaluator model with zero temperature to ensure reproducible evaluation scores across runs.
6. **Decoupled System Architecture:** Separated generation logic (`agent.py`) from scoring logic (`evaluator.py`) to allow independent benchmark runs.
7. **Explicit Boundary System Prompts:** Instructed the model to acknowledge scope limits explicitly rather than making speculative guesses on out-of-scope topics.
8. **Subsampling Strategy:** Evaluated against a curated 30-item Golden Set containing representative edge cases rather than uncurated dataset noise.
9. **JSON Output Schema:** Enforced strict output parsing on evaluator outputs to prevent evaluation script execution crashes.
10. **Environment Separation:** Kept workspace credentials and platform configurations isolated in dedicated `.env` configurations.

## 4. Roadmap (What to Build with One More Week)
* **Hybrid Search Retrieval:** Combine BM25 keyword matching with dense vector retrieval to better capture technical error codes (e.g., `HTTP 403`).
* **Stateful Multi-Turn Conversations:** Introduce session management to persist context across multi-turn support conversations.
* **Human-in-the-Loop Routing:** Implement automated low-confidence triggers to automatically escalate ambiguous or hostile queries to human support agents.
