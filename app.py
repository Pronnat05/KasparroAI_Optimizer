import streamlit as st
import json
import time
from Scanner import ShopifyScanner
from agents import auditor

st.set_page_config(
    page_title="Shopify Optimizer 2026",
    layout="wide",
    initial_sidebar_state="expanded"
)

#-----Theme
st.markdown("""
    <style>
    /* Main Background & Fonts */
    .stApp {
        background: linear-gradient(135deg, #0d0f14 0%, #151922 100%);
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: #e2e8f0;
    }

    /* Header and Subtitles Styling */
    h1 {
        font-weight: 800 !important;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }

    /* Sidebar Futuristic Look */
    [data-testid="stSidebar"] {
        background-color: #090b0f !important;
        border-right: 1px solid #1e2633;
    }

    /* Elegant Cards Layout (Glassmorphism Effect) */
    .metric-box { 
        padding: 20px; 
        border-radius: 12px; 
        background: rgba(30, 34, 43, 0.4); 
        backdrop-filter: blur(10px);
        margin-bottom: 15px; 
        border: 1px solid rgba(255, 75, 75, 0.2);
        box-shadow: 0 4px 20px rgba(255, 75, 75, 0.05);
    }
    .metric-box-warn { 
        padding: 20px; 
        border-radius: 12px; 
        background: rgba(30, 34, 43, 0.4); 
        backdrop-filter: blur(10px);
        margin-bottom: 15px; 
        border: 1px solid rgba(255, 165, 0, 0.2);
        box-shadow: 0 4px 20px rgba(255, 165, 0, 0.05);
    }
    .metric-box-info { 
        padding: 20px; 
        border-radius: 12px; 
        background: rgba(30, 34, 43, 0.4); 
        backdrop-filter: blur(10px);
        margin-bottom: 15px; 
        border: 1px solid rgba(31, 119, 180, 0.2);
        box-shadow: 0 4px 20px rgba(31, 119, 180, 0.05);
    }

    /* Custom Neon Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.3) !important;
        transition: all 0.3s ease-on-out !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.5) !important;
    }

    /* Smooth Expander Panels */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1f2c !important;
        border-radius: 6px 6px 0px 0px;
        padding: 10px 20px !important;
        color: #a0aec0 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: #000000 !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Kasparro AI Representation Optimizer")
st.subheader("Transitioning Shopify Stores from 'Search-and-Browse' to 'Ask and Decide' ")
st.markdown("---")

# ---Sidebar
st.sidebar.header("⚙️ Control Panel")
st.sidebar.info("Auditing platform compliant with Shopify Agentic Plan & Universal Commerce Protocol (UCP).")
run_audit = st.sidebar.button("⚡ Run Store AI Audit", use_container_width=True)

if run_audit:
    with st.spinner("Step 1: Fetching store data via GraphQL Admin API..."):
        scanner = ShopifyScanner()
        try:
            store_data = scanner.fetch_products()
        except Exception as e:
            st.error(f"Shopify Connection Failed: {e}")
            store_data = None

    if store_data and store_data.get('products', {}).get('edges'):
        products = store_data['products']['edges']

        total_products = len(products)
        all_results = []

        with st.spinner("Step 2: Orchestrating TaskAssistant Agent & analyzing gaps..."):
            for edge in products:
                p = edge['node']
                raw_analysis = auditor.audit_with_ai(p)
                try:
                    analysis_json = json.loads(raw_analysis)
                    analysis_json['title'] = p['title']
                    analysis_json['old_desc'] = p['description']
                    all_results.append(analysis_json)
                except Exception as parse_error:
                    st.warning(f"Failed to parse analysis for {p['title']}. Retrying standard structure.")


                time.sleep(12)

        # --ScoreCard
        if all_results:
            avg_score = int(sum(r['score'] for r in all_results) / len(all_results))

            st.header("📊 Global Store Insights")
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric(label="Total Audited Products", value=total_products)
            with col_m2:
                st.metric(label="Global AI Readiness Score", value=f"{avg_score}%",
                          delta=f"{avg_score - 100}% From Perfect Indexing")
            with col_m3:
                if avg_score < 50:
                    st.error("🚨 Action Required: High Hallucination Risk")
                elif avg_score < 80:
                    st.warning("⚠️ Partial Discovery: Missing Core Trust Signals")
                else:
                    st.success("✅ Universal Commerce Protocol Ready")

            st.markdown("---")

            # --Product Analysis
            st.header("🎯 Granular Product Diagnostics")

            for result in all_results:
                with st.expander(f"📋 Audit Overview: {result['title']} (Readiness: {result['score']}%)"):
                    diagnosis_tab, action_tab = st.tabs(["🔍 AI Perception Diagnosis", "🛠️ Merchant Action Playbook"])

                    with diagnosis_tab:
                        st.write("### **How AI Agents See This Product:**")
                        st.info(result.get('perception_summary', 'No perception summary generated.'))
                        raw_gaps = result.get('gaps', [])
                        if not raw_gaps:
                            raw_gaps = result.get('high_priority', []) + result.get('medium_priority', []) + result.get(
                                'low_priority', [])
                        total_gaps_count = len(raw_gaps)
                        if total_gaps_count >= 3:
                            split_size = total_gaps_count // 3
                            high_gaps = raw_gaps[:split_size]
                            med_gaps = raw_gaps[split_size:2 * split_size]
                            low_gaps = raw_gaps[2 * split_size:]
                        else:
                            high_gaps = raw_gaps
                            med_gaps = []
                            low_gaps = []

                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.markdown("<div class='metric-box'><strong>🚨 High Priority Gaps</strong></div>",
                                        unsafe_allow_html=True)
                            if high_gaps:
                                for gap in high_gaps:
                                    st.error(f"• {gap}")
                            else:
                                st.info("No critical infrastructure gaps detected.")

                        with c2:
                            st.markdown("<div class='metric-box-warn'><strong>⚠️ Medium Priority Gaps</strong></div>",
                                        unsafe_allow_html=True)
                            if med_gaps:
                                for gap in med_gaps:
                                    st.warning(f"• {gap}")
                            else:
                                st.info("No alignment gaps detected.")

                        with c3:
                            st.markdown("<div class='metric-box-info'><strong>💡 Low Priority Gaps</strong></div>",
                                        unsafe_allow_html=True)
                            if low_gaps:
                                for gap in low_gaps:
                                    st.info(f"• {gap}")
                            else:
                                st.info("No enrichment gaps detected.")

                    with action_tab:
                        st.write("### **Ranked Action Items:**")
                        action_items = result.get('action_plan', [])
                        if action_items:
                            for item in action_items:
                                st.markdown(f"- {item}")
                        else:
                            st.write(result.get('optimized_description', 'No explicit optimization plan generated.'))

                        st.success(
                            "💡 **Conversion Insight:** Resolving these structured elements provides deterministic parameters for AI LLM context windows, maximizing checkout recommendation rates.")
    else:
        st.error(
            "No active products or shop details retrieved. Please verify your token permissions and active listings.")

st.sidebar.markdown("---")
st.sidebar.caption("Developer: PRONNAT MOHAN")