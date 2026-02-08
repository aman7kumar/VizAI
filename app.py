import streamlit as st
import pandas as pd
import plotly.io as pio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from modules.auth import login, check
login()

if not check():
    st.stop()


from modules.llm import generate_code
from modules.e2b_runner import execute_code
from modules.history import add_history, get_history
from modules.pdf_report import create_pdf

# ---------------- PAGE TITLE ----------------
st.title("VizAI – AI Data Visualization Agent (Groq Powered)")

# ---------------- CLEAR DASHBOARD ----------------
if st.button("Clear Dashboard"):
    st.session_state.results = []

# ---------------- FILE UPLOAD ----------------
file = st.file_uploader("Upload CSV File")

if file:
    df = pd.read_csv(file)

    st.write("Dataset Preview")
    st.dataframe(df.head())


    # ========== ADD SQL / NL MODE SWITCH HERE ==========
    mode = st.radio("Mode", ["Natural Language", "SQL"])

    # ---------------- SQL MODE ----------------
    if mode == "SQL":

        st.info("Table name for SQL = data")

        sql = st.text_area("Write SQL Query")

        if st.button("Run SQL"):
            from modules.sql_engine import query_sql

            res = query_sql(df, sql)

            st.subheader("SQL Result")
            st.write(res)

        # STOP further execution when in SQL mode
        st.stop()

    # ---------------- NATURAL LANGUAGE MODE ----------------
    query = st.text_input("Ask anything about your data")

    if query:

        # ----- Generate code -----
        code = generate_code(query, list(df.columns))

        st.subheader("Generated Code")
        st.code(code)

        # ----- Execute -----
        result = execute_code(code, df)

        # ----- Init session -----
        if "results" not in st.session_state:
            st.session_state.results = []

        # ----- Error handling -----
        if isinstance(result, dict) and "error" in result:
            st.error(result["error"])

        else:
            # Save HTML for report (no kaleido)
            try:
                if result.get("figures"):
                    pio.write_html(result["figures"][0], "chart.html")
            except:
                pass

            # Save to session
            st.session_state.results.append({
                "query": query,
                "result": result
            })

            add_history(query, "Visualization generated")

            # ----- PDF DOWNLOAD -----
            if st.button("Download Report"):
                pdf = create_pdf(query, "Visualization Report", "chart.html")

                with open(pdf, "rb") as f:
                    st.download_button(
                        label="Download PDF",
                        data=f,
                        file_name=pdf
                    )

# =================================================
#           MULTI-CHART DASHBOARD SECTION
# =================================================

if "results" in st.session_state:

    for item in st.session_state.results:

        st.markdown("---")
        st.subheader(f"Query: {item['query']}")

        tabs = st.tabs(["Charts", "Insights"])

        # -------- TAB 1 : CHARTS --------
        with tabs[0]:

            figs = item["result"].get("figures", [])

            if figs:
                for fig in figs:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No charts generated")

        # -------- TAB 2 : INSIGHTS --------
        with tabs[1]:

            texts = item["result"].get("text", [])

            if texts:
                for t in texts:
                    st.info(t)
            else:
                st.write("No insights generated")

# ---------------- SIDEBAR HISTORY ----------------
st.sidebar.title("Chat History")
st.sidebar.write(get_history())
