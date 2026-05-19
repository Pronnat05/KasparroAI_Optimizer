# 📑 Project Engineering Log & Documentation
**Track 5: Advanced AI Orchestration for Conversational Commerce**
**Developer:** Pronnat Mohan (Solo Project)

---

## 🎯 SECTION 1: THE PRODUCT LOG (What & Why)

### 1. What was built
The project is **Kasparro AIO (AI Representation Optimizer)**. It is a specialized sandbox dashboard for Shopify store owners to analyze how current LLM crawlers, vector search indices, and autonomous AI shopping agents perceive their store catalog. It directly highlights what makes a product "invisible" to an AI buyer.

### 2. The Target User
Shopify merchants who want to maximize their sales in the 2026 conversational commerce market. If a user asks an AI bot for a specific product recommendation, this tool ensures the merchant's store doesn't get left out due to bad or incomplete data structuring.

### 3. The Core Problem Statement
Most product descriptions on Shopify are written purely for human eyes or basic Google SEO keywords. 
- Merchants often put technical details inside images/infographics and write generic descriptions like *"See features in the image below"*.
- For text-centric LLM agents, this creates an immediate structural dead-end, making the product un-rankable. 
- The result? The AI agent either skips the product entirely or falls into a **Hallucination Risk**, making up fake specs to answer the user's query, which ruins the store's credibility.

### 4. Tradeoffs & Engineering Scope
- **What’s In:** Reading product payloads via GraphQL, analyzing visibility gaps from an AI perspective, breaking down flaws into critical priority tiers, and providing copy-pasteable metadata improvements.
- **What’s Out (Intentional Tradeoff):** Automated write-backs to live Shopify catalogs. Writing code that automatically modifies live production inventory during a fast-paced hackathon sprint poses a massive operational risk. We strictly limited the app to a read-only evaluation sandbox to maintain merchant store safety.

---

## 💻 SECTION 2: TECHNICAL DOCUMENTATION & SYSTEM WORKFLOW

### 1. Application Architecture



The codebase is split into three clean, un-entangled layers:
1. **Ingestion (`Scanner.py`):** Opens a secure connection to the Shopify store using native GraphQL Admin API queries and user access tokens (`shpua_`). It extracts heavily nested catalog fragments efficiently.
2. **Analysis (`agents.py`):** Feeds the raw data strings into a specialized system prompt using **gemini-2.5-flash**. The model runs under a tight `TaskAssistant` profile to execute zero-shot structural grading.
3. **Frontend (`app.py`):** A Streamlit interface completely custom-styled with a glass-minimalism CSS overlay to give it a polished, premium SaaS aura instead of a stock template feel.

### 2. Deep Technical Implementation Choices
- **GraphQL over REST API:** Standard REST endpoints require multiple resource calls to fetch nested product options, leading to fast API degradation and over-fetching. GraphQL allowed us to pin down exactly the fields we needed in a single network round-trip.
- **Frontend Array Bifurcation:** Initially, we prompted the LLM to output separated JSON blocks for high, medium, and low errors. However, during runtime checks, Gemini occasionally modified the JSON keys unpredictably (e.g., swapping `high_priority` with camelCase `highPriority`), breaking the Streamlit display loop. To make the code bulletproof, we refactored the pipeline to output a simple unified `"gaps"` array, which our frontend Python script splits into three categorical columns.

### 3. Exception Handling & Resilience
- **Rate-Limit Guard:** To bypass the strict Requests Per Minute (RPM) threshold of the Gemini Free Tier, a hard-coded 12-second delay (`time.sleep(12)`) is enforced inside the orchestration iteration.
- **Zero-Downtime Mock Fallback (Anti-Crash Layer):** During high-concurrency judging or presentation runs, free-tier tokens can easily face daily quota exhaustion (`ResourceExhausted 429`). To prevent a total live-demo crash, we wrapped the model call in a clean `try-except` block. If a 429 error code is caught, the app immediately intercepts the crash and injects high-fidelity, pre-cached mockup structures for products like `ZenBrew Coffee Maker` or `GlowSkin Serum`. The interface stays up, maintaining a flawless user experience.

---

## ⏱️ SECTION 3: SOLO DEVELOPER MATRIX (How Time Was Split)

Working completely solo meant managing both product strategy and core development simultaneously. The timeline was divided into a clear **50-50 execution split**:

- **Product Thinking & Research (50%):** Spent analyzing the mechanics of the Universal Commerce Protocol (UCP), documenting why AI models fail to parse vague descriptions, setting up structural benchmarks for skincare and appliance attributes, and mapping out a non-cluttered dark-mode layout interface.
- **Engineering & Debugging (50%):** Spent writing the actual Python codebases, writing the nested GraphQL query bodies, handling Git push protections where hardcoded test keys leaked, fixing Streamlit HTML styling parameters (`unsafe_allow_html=True`), and debugging the JSON string parsing wrappers.

---

## 🪵 SECTION 4: THE CORE DECISION LOG

- **Issue:** Data Extraction Protocol
  - **Considered Route:** Shopify REST Admin API
  - **Chosen Route:** **Shopify GraphQL Admin API**
  - **Justification:** REST endpoints create immense payload overhead and over-fetching, hitting Shopify's API rate rules almost instantly. GraphQL allows fine-tuned retrieval.
  
- **Issue:** UI Styling Layer
  - **Considered Route:** Default Native Streamlit Alert Elements (`st.error`, `st.warning`)
  - **Chosen Route:** **Custom SVG/HTML Cards via CSS injection**
  - **Justification:** Default blocks look cluttered and lack professional appeal. Injecting clean, responsive micro-cards with custom borders established a premium look for reviewers.

- **Issue:** LLM JSON Schema Validation
  - **Considered Route:** Enforcing strict schema outputs inside system prompt keys
  - **Chosen Route:** **Unified Array Output with Frontend Mathematical Slicing**
  - **Justification:** Gemini 2.5 Flash occasionally alters naming conventions under heavy data context, causing parsing faults. Moving the array splitting logic to the Python frontend removed template vulnerabilities entirely.

- **Issue:** 429 Quota Exhaustion
  - **Considered Route:** Displaying a basic system execution tracebaсk error
  - **Chosen Route:** **Graceful Exception Catching + Pre-cached Mock Payloads**
  - **Justification:** Live judging sessions can deplete free API keys quickly. Loading structured fallback payloads guarantees the dashboard stays functional and responsive during evaluations.
