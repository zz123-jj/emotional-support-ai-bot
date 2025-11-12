# Group Report – Design & Planning, Documentation & Analysis

## 1. Design and Planning (Assessment Criterion: Design & Planning – LO B, C, D, F)

### 1.1 Vision and Problem Statement
Emotional Support Learning Companion helps university students manage study-related emotional challenges (anxiety, pressure, isolation, frustration). It delivers empathetic, context-aware guidance by combining Generative AI (GPT-4o-mini), Retrieval-Augmented Generation (RAG), prompt engineering, and continuous learning to ground responses in credible coping strategies.

### 1.2 User-Centered Design Approach (LO C)
- Personas: (1) First-year student overwhelmed by coursework; (2) Senior under deadlines; (3) International student facing isolation.
- Needs: Emotional validation, actionable coping steps, low-friction access, clear privacy.
- Principles: Empathy-first tone, minimal cognitive load, clear affordances, transparent scope (not a diagnostic tool).
- Ethics: Avoid clinical claims; recommend professional help for crisis; local data storage; culturally sensitive language.

### 1.3 User Interface and Interaction Flow (LO C, D)
Gradio web UI with four tabs:
1) Chat: message → emotion detection → RAG retrieval → prompt assembly → GPT-4o-mini response → optional rating (1–5).
2) Analytics Dashboard: emotion distribution, average feedback score, session counts, trend lines.
3) Learning Center: manually trigger knowledge extraction from high-rated interactions (≥4).
4) Help/Guide: usage scope, privacy, limitations, escalation guidance.

Flow: User Message → Emotion Analysis → Top-K Retrieval → Dynamic Prompt → Generation → Display → Feedback → Learning Buffer → Knowledge Base Update.

### 1.4 Data Sources and Requirements (LO D)
- Inputs: user text, derived emotion tags, curated coping knowledge base, feedback scores, timestamps/session IDs.
- Requirements: anonymized logs, traceability for enrichment, separation of transient context vs persistent records.
- Collection: persist message-response pairs (SQLite); log emotion trends; queue high-score interactions for learning.
- Processing: keyword emotion tagging; semantic retrieval via `all-MiniLM-L6-v2` + ChromaDB; extract Q/A exemplars.
- Usage: immediate grounding and personalization; deferred enrichment; analytics for user reflection.
- Privacy & risk: local storage; minimal external sharing (OpenAI API for generation only); crisis disclaimers; avoid PII.

### 1.5 AI Model Selection Justification (LO B, D)
- Generative Core: GPT-4o-mini — strong coherence and empathy at lower cost/latency than full GPT-4; suitable for iterative prototyping.
- Embeddings: Sentence Transformers `all-MiniLM-L6-v2` — ~90MB, multilingual, fast; meets interactive latency goals.
- Vector Store: ChromaDB — simple Python API, persistent local storage, efficient similarity search.
- Alternatives: BERT (non-generative), larger sentence-transformers (heavier downloads), full GPT-4 (higher cost/latency). Trade-offs are mitigated by RAG grounding and continuous KB enrichment.

### 1.6 Prompt Engineering Strategy (LO B)
1) System role prompt with guardrails and empathy guidance.
2) Last 10 turns of conversation for continuity.
3) Injected Top-K RAG snippets (default 3).
4) Current user query.
Tone adapts to detected emotions; high-scored outputs are more likely to become retrievable exemplars.

### 1.7 Tools and Technologies Rationale (LO D)
- Python, Gradio, OpenAI SDK, Sentence Transformers, ChromaDB, SQLite, SQLAlchemy, optional LangChain modules.
- Scalability path: SQLite → PostgreSQL; ChromaDB → managed vector DB; add caching and streaming; persona profiles for personalization.

### 1.8 Role Assignment and Rotation (LO F, EDI)
- Roles: Project Lead/Facilitator; AI Engineer; Retrieval & Data Engineer; UX/UI Designer; Ethics & Safety Champion; QA & Evaluation Lead.
- Rotation: bi-weekly shadowing and partial responsibility transfer; pairing (Lead↔Ethics, AI↔Data, UX↔QA).
- EDI: equal speaking time, anonymous idea intake before critique, async-friendly processes, psychological safety.
- Deliverables per cycle: updated prompts & output logs (AI), retrieval latency & enrichment delta (Data), wireframes & journeys (UX), risk log & mitigations (Ethics), coverage & defect summary (QA).

### 1.9 Risk Mitigation Summary (LO D)
- Hallucination → RAG grounding, explicit disclaimers.
- Emotional harm → empathy guardrails, crisis escalation info.
- Data leakage → local-only storage, minimal external calls.
- Bias → diverse knowledge curation, ethics reviews.
- Over-reliance → nudge toward professional resources.
- Scale limits → modular design, documented upgrade path.

---

## 2. Documentation and Analysis (Assessment Criterion: Documentation & Analysis – LO B, D, E)

### 2.1 Technical Design Overview
Core modules: `chatbot.py` (orchestrator), `prompt_engineering.py` (prompt builder + emotion analyzer), `rag_system.py` (embedding + vector search via ChromaDB), `data_system.py` (SQLite + learning), `app.py` (Gradio UI). Data flow: Input → Emotion Analysis → Retrieval → Prompt Assembly → GPT-4o-mini → Logging → Feedback → Knowledge Extraction → KB Augmentation.

### 2.2 AI Integration Plan
- Pre-processing: emotion tags frame the response style.
- Retrieval: Top-K semantic snippets reduce hallucination.
- Generation: GPT-4o-mini produces empathetic, grounded replies.
- Post-processing: log results, capture feedback, trigger learning when threshold met.
- Extensible: add classifier-based sentiment, streaming, user personas; upgrade emotion detection beyond keywords.

### 2.3 Preliminary Evaluation Plan
1) Functional Accuracy: 20 curated queries; Top-3 retrieval relevance ≥85%.
2) Response Quality: human rating (1–5) on empathy/relevance/clarity; average ≥4.0.
3) Latency: P95 < 4s over 30 requests.
4) Continuous Learning Impact: before/after enrichment deltas on relevance & satisfaction.
5) Safety/Ethics: red-team prompts (crisis/unsafe); required boundary and resource guidance.
6) Robustness: empty/long/mixed-language inputs handled safely.
7) Data Integrity: schema-consistent logging and feedback linkage (100%).
8) Bias Scan: qualitative review of demographic prompts; document and mitigate.
Artifacts: test matrix, sample outputs, performance logs, risk register.

### 2.4 Communication Plan (LO E)
- Written: structured Markdown with diagrams (architecture, RAG pipeline, evaluation matrix).
- Oral: 8–10 min presentation (Problem → Approach → Impact → Ethics) with clear visuals.
- Inclusive language and definition of acronyms on first use.

---

## 3. Learning Outcomes Mapping (A–F)
- A: GAI concepts and applications explained via model choice and use cases (Sections 1.1, 1.5).
- B: Prompt engineering + RAG design and evaluation methods (Sections 1.6, 2.3).
- C: User-centered design and ethics guardrails (Sections 1.2–1.3).
- D: Comprehensive plan for data, models, UI, deployment path, and risks (Sections 1.4–1.9, 2.1–2.3).
- E: Clear written structure and presentation strategy (Section 2.4).
- F: Team role assignment, rotation, and EDI practices (Section 1.8).

---

## 4. Future Enhancements
- Transformer-based emotion classifier; multilingual dynamic embeddings.
- User preference personalization; streaming responses.
- Privacy-preserving analytics (e.g., differential privacy);
- Real-time moderation filters.
