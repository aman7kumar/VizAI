import streamlit as st
import pandas as pd
import plotly.io as pio
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

from modules.auth import login, check

# Default Page Config
st.set_page_config(
    page_title="VizAI - AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS For Modern UI ----------------
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(17, 24, 39) 0%, rgb(0, 0, 0) 90%);
        color: #ffffff;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }

    /* Titles and Headers */
    h1, h2, h3 {
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
        border-radius: 8px;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 10px;
    }

    /* Cards/Containers */
    .css-1r6slb0 {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)


# Application Logic
login()

if not check():
    st.stop()

from modules.llm import generate_code
from modules.e2b_runner import execute_code
from modules.history import add_history, get_history
from modules.pdf_report import create_pdf


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📊 VizAI")
    st.markdown("Your AI-powered data visualization assistant.")
    st.markdown("---")
    
    st.subheader("History")
    st.write(get_history())
    
    st.markdown("---")
    st.info("💡 Tip: Be specific with your queries for better charts.")


# ---------------- MAIN CONTENT ----------------
# Header
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("VizAI: Insight Engine")
    st.markdown("Upload your data and let AI visualize it for you.")

with col2:
    if st.button("Clear Dashboard", type="secondary"):
        st.session_state.results = []
        st.rerun()

st.markdown("---")

# File Upload Section
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if file:
    st.session_state.uploaded_file = file
    df = pd.read_csv(file)

    # Data Preview
    with st.expander("👀 View Dataset Preview", expanded=False):
        st.dataframe(df, use_container_width=True)
        st.caption(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")

    # Mode Selection
    st.markdown("### 🛠 Select Mode")
    mode = st.radio("Choose interaction mode:", ["Natural Language", "SQL Query"], horizontal=True, label_visibility="collapsed")

    # ---------------- SQL MODE ----------------
    if mode == "SQL Query":
        st.info("📝 Table name for SQL is `data`")
        
        sql = st.text_area("Write SQL Query", height=150, placeholder="SELECT * FROM data WHERE...")
        
        if st.button("Run SQL Query", type="primary"):
            from modules.sql_engine import query_sql
            with st.spinner("Running SQL Query..."):
                try:
                    res = query_sql(df, sql)
                    st.success("Query Executed Successfully!")
                    st.subheader("Result")
                    st.dataframe(res, use_container_width=True)
                except Exception as e:
                    st.error(f"Error executing SQL: {e}")

    # ---------------- NATURAL LANGUAGE MODE ----------------
    else:
        query = st.chat_input("Ask a question about your data (e.g., 'Show me sales over time')")

        if query:
            # Display user message
            with st.chat_message("user"):
                st.write(query)

            # Process query
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Thinking... 🧠")
                
                # Generate Code
                try:
                    code = generate_code(query, list(df.columns))
                    
                    # Execute Code
                    result = execute_code(code, df)
                    
                    if isinstance(result, dict) and "error" in result:
                        message_placeholder.error(f"Error: {result['error']}")
                    else:
                        message_placeholder.success("Visualization Generated!")
                        
                        # Init session
                        if "results" not in st.session_state:
                            st.session_state.results = []

                        # Save result logic
                        try:
                            if result.get("figures"):
                                pio.write_html(result["figures"][0], "chart.html")
                        except:
                            pass
                            
                        st.session_state.results.append({
                            "query": query,
                            "result": result
                        })
                        add_history(query, "Visualization generated")
                        
                        # Show current result immediately
                        tabs = st.tabs(["📊 Chart", "💡 Insights", "💻 Code"])
                        with tabs[0]:
                            if result.get("figures"):
                                st.plotly_chart(result["figures"][0], use_container_width=True)
                            else:
                                st.warning("No chart generated.")
                        with tabs[1]:
                             if result.get("text"):
                                for t in result["text"]:
                                    st.info(t)
                             else:
                                st.write("No text insights.")
                        with tabs[2]:
                            st.code(code, language='python')
                            
                except Exception as e:
                    message_placeholder.error(f"An error occurred: {e}")

# ---------------- DASHBOARD (PAST RESULTS) ----------------
if "results" in st.session_state and st.session_state.results:
    st.markdown("---")
    st.subheader("📌 Dashboard")
    
    # Show past results in reverse order (newest first)
    for i, item in enumerate(list(reversed(st.session_state.results))):
        if i == 0 and mode != "SQL Query" and query: continue # Skip the one just shown if we are in interaction loop (simplified)
        
        with st.expander(f"Q: {item['query']}", expanded=False):
            tabs = st.tabs(["📊 Chart", "💡 Insights"])
            with tabs[0]:
                figs = item["result"].get("figures", [])
                if figs:
                    for fig in figs:
                        st.plotly_chart(fig, use_container_width=True)
            with tabs[1]:
                texts = item["result"].get("text", [])
                for t in texts:
                    st.write(t)

