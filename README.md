# Analogy Schema: Causal-Event Graph Induction from Narrative Text

A scientific NLP framework for **analogical reasoning and abstract schema induction from narrative text**. 

Rather than relying on direct black-box classification, this system independently induces an **abstract causal-event graph** from each narrative. These grounded representations isolate the core explanatory mechanism of the story (problems, interventions, constraints, focal outcomes, and contingent consequences) into a minimal causal backbone suitable for cross-domain structural alignment.

---

## 🔬 Core Induction Pipeline (Stages A–H)

The system transforms raw narrative text into a structured causal backbone through eight discrete stages with deterministic graph algorithms and Pydantic v2 schemas:

```text
Story Text
   │
   ├── [Stage A] Atomic Event Extraction (High recall, textual grounding, explicit/inferred)
   │
   ├── [Stage B] Semantic Predicate Normalization + Temporal Grounding (Mention vs. Onset)
   │
   ├── [Stage C & D Concurrent Execution]
   │     ├─ [Stage C] Evidence-Grounded Typed Relation Extraction (Causal & Temporal ontology)
   │     └─ [Stage D] Narrative Anchors & Structured Incentive Contract Identification
   │
   ├── [Stage E] Backward Multi-Track Causal Tracing (Deterministic NetworkX traversal)
   │
   ├── [Stage F] Counterfactual Explanatory Backbone Selection & Pruning
   │
   ├── [Stage G & H] Macro-Node Grouping, 4-Level Abstraction Ladders & Rich-Edge Lifting
   │
   └── [Minimality Pass] Topological Minimality & Invariant Validation
```

---

## 🌟 Methodological Highlights

1. **Zero Ground-Truth Leakage Shield**:
   - Stories are presented to LLMs via an anonymous `StoryInput` containing strictly `story_id`, `text`, and sentence segmentation.
   - All ground-truth benchmark labels (`True Analogy`, `False Analogy`, `Literally Similar`, etc.) are completely quarantined in [`analogy_schema/fixtures/benchmark_manifest.json`](analogy_schema/fixtures/benchmark_manifest.json).
2. **Disambiguated Intervention-Relative Time (`TemporalGrounding`)**:
   - Separates textual mention position (`mention_phase`) from true story-world initiation (`onset_phase`).
   - Explicitly models persistent states that hold when an intervention is introduced (`holds_at_intervention=True`).
3. **Programmatic Anti-Merging Invariant**:
   - Events connected by rich relations (`CAUSES`, `RESULTS_IN`, `BLOCKS`, `PREVENTS`, `ENABLES`, `MOTIVATES`, `REQUIRES`, `BEFORE`) are strictly barred from merging into composite macro-nodes, preserving causal topology.
4. **Pure Atomic Functional Labels**:
   - Level-2 labels represent atomic states/events (e.g. `task neglect`, `performance deficit`, `conditional incentive`, `requirement failure`, `reward withheld`) with all embedded relational connectives (`"caused by"`, `"due to"`, `"leading to"`) strictly sanitized.
5. **Separated Explanatory Edges vs. Minimal Temporal Constraints**:
   - Causal/functional mechanisms are categorized under `explanatory_edges`.
   - Chronological ordering is categorized under `temporal_constraints` and minimized via `networkx.transitive_reduction`.
6. **Structured Incentive Contracts**:
   - Contingencies are modeled as structured contract metadata (`IncentiveContract(promised_reward, contingent_requirement, condition_polarity)`), preserving consequential outcomes as concrete relations.
7. **Two-Level Concurrency**:
   - **Intra-Pipeline**: Stages C & D run in parallel via `asyncio.gather()`.
   - **Inter-Story**: Batch runner processes multiple narratives simultaneously using `asyncio.Semaphore`.

---

## 📁 Repository Structure

```text
analogy-schema/
├── analogy_schema/
│   ├── models/                  # Core Pydantic schemas (story, events, relations, backbone)
│   ├── pipeline/                # Stages A through H + SingleStoryPipeline runner
│   ├── prompts/                 # Neutral, leak-free prompt registry templates
│   ├── llm/                     # Async LLM Providers (OpenRouter with DeepSeek-v4-flash, Mock)
│   ├── utils/                   # Serialization, graph algorithms, DAG validators
│   └── fixtures/                # Benchmark narratives and quarantined manifest
│       ├── stories/             # 6 verbatim benchmark stories + 3 synthetic stories
│       └── benchmark_manifest.json
├── outputs/                     # Generated JSON graphs and human-readable summaries
├── visualizer/                  # Self-contained local Cytoscape.js directed graph explorer
│   ├── server.py                # REST API backend & static file server
│   ├── adapters.py              # Pure read-only JSON schema adapters
│   └── static/                  # Single-page UI (HTML, CSS, JS)
├── tests/                       # Unit and causal-stability regression test suite
├── run_pipeline.py              # CLI runner for single stories
├── run_batch.py                 # Concurrent multi-story batch runner
├── run_visualizer.py            # Entry point for the local graph explorer
├── pyproject.toml
└── README.md
```

---

## 🚀 Quickstart

### 1. Environment Setup

Configure your `.env` file in the project root:

```bash
OPENROUTER_API_KEY="your-openrouter-api-key"
```

The system uses `deepseek/deepseek-v4-flash` via OpenRouter with reasoning disabled for fast, deterministic structured extraction.

### 2. Run Tests

Execute the comprehensive unit and causal stability regression suite:

```bash
pytest -v
```

---

## 🏃 Running the Pipeline

### Option A: Run All 6 Exact Benchmark Narratives in Parallel (Fastest)

Process all 6 benchmark stories concurrently with 6 worker threads:

```bash
python3 run_batch.py --benchmarks --concurrency 6
```

### Option B: Run Synthetic Fixtures

```bash
python3 run_batch.py --synth --concurrency 3
```

### Option C: Run a Single Story

```bash
python3 run_pipeline.py --story analogy_schema/fixtures/stories/story_base_01.json
```

Outputs are automatically saved to `outputs/<story_id>/`:
* `causal_backbone.json`: Final abstract causal-event graph.
* `rich_event_graph.json`: Pre-backbone normalized event and relation graph.
* `backbone_summary.md`: Human-inspectable markdown summary with provenance and ladders.

---

## 🌐 Local Graph Explorer (Visualizer)

The project includes an interactive, dependency-free graph inspection tool for debugging induced graphs:

```bash
python3 run_visualizer.py
```

Then open:
```text
http://localhost:8000
```

### Visualizer Features:
* **Dynamic Output Discovery**: Automatically detects any folder generated in `outputs/`.
* **Dual View**: Toggle between **Causal Backbone** and **Rich Event Graph**.
* **Edge Category Filtering**: Checkboxes to toggle Explanatory Causal Edges vs. Temporal (`BEFORE`) Constraints.
* **4-Level Abstraction Inspector**: Inspect Level 0 (Raw), Level 1 (Domain), Level 2 (Functional), and Level 3 (Schema).
* **Live Provenance Highlighter**: Clicking any node highlights its verbatim source text span in the original narrative panel.
* **Incentive Contracts & Anchors**: Structured contract terms, central problems, goals, and pruned event audit trails.
* **Validation Warnings Banner**: Prominent reporting of any topological or semantic invariant warnings.

---

## 📜 4-Level Abstraction Ladder Standard

| Level | Abstraction Type | Description | Example |
| :--- | :--- | :--- | :--- |
| **Level 0** | **Raw / Literal** | Literal story text phrasing | *"William spent his time daydreaming about food"* |
| **Level 1** | **Domain Predicate** | Domain-specific semantic predicate | *"William neglects cleaning room"* |
| **Level 2** | **Functional Role** | Cross-domain atomic functional description (target level) | `task neglect` |
| **Level 3** | **Abstract Schema** | High-level generalized schema | `inaction` |
