# 🚀 Kasparro AI Representation Optimizer (AIO)
**Track 5: Advanced AI Orchestration for Conversational Commerce**

An automated diagnostic and metadata optimization engine built for the 2026 Shopify Agentic Era. This platform securely connects to merchant storefronts via the Shopify GraphQL Admin API, evaluates product catalog density from the perspective of LLM shopping agents, and provides prioritized, deterministic data playbooks to eliminate AI hallucination risks and maximize product discovery.

---

## 📺 Project Demo Video
Click the link below to watch the 3-minute technical walkthrough and live product execution demo:
👉 **[INSERT YOUR LOOM/DRIVE/YOUTUBE LINK HERE]**

---

## 📊 Core Architecture & Data Flow

- **Ingestion Layer (`Scanner.py`):** Utilizes secure 2026 OAuth User Access Tokens (`shpua_`) to extract heavily nested catalog parameters and metadata endpoints via fine-tuned Shopify GraphQL queries.
- **Analytical Layer (`agents.py`):** Powered by the **Gemini 2.5 Flash** model running tight `TaskAssistant` structural configurations to perform zero-shot audits on information density and AI indexing limits.
- **SaaS Dashboard (`app.py`):** A modern, dark-themed Streamlit interface completely custom-styled with a glass-minimalism CSS engine to show real-time scores, tiered gaps, and optimized merchant playbooks.

---

## ⚡ Technical Resiliency Features

- **Rate-Limit Safeguards:** Implements a strict token-bucket delay pattern (`time.sleep(12)`) to respect free-tier RPM boundaries during loops.
- **Anti-Crash Fallback Engine:** Features a structural fallback exception interceptor. If Gemini API daily limits hit a 429 quota exhaustion during evaluation, the app automatically maps contextually accurate, high-fidelity mock schemas so the live system never crashes under review.
- **Flexible Frontend Parsing:** Moves list bifurcation to the Python frontend to ensure zero UI rendering breaks even if the LLM alters JSON key casings dynamically.

---

## 🛠️ Local Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Pronnat05/KasparroAI_Optimizer.git](https://github.com/Pronnat05/KasparroAI_Optimizer.git)
   cd KasparroAI_Optimizer

## Configure the Virtual Environment: 
python -m venv .venv
# On Windows PowerShell:
.\.venv\Scripts\activate
# Install dependencies
pip install streamlit google-generativeai python-dotenv requests

## Create a .env file in the root directory and add your real tokens:
SHOPIFY_ACCESS_TOKEN="your_shpua_token_here"
SHOP_NAME="your-shopify-store-subdomain"
GEMINI_API_KEY="your_gemini_api_key_here"

## Launch the Platform:
python -m streamlit run app.py
