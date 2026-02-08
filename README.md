# <u>📊 **VizAI – AI Data Visualization Agent**</u>

This Streamlit application creates an interactive Data Visualization Assistant that can understand Natural Language Queries and generate appropriate visualizations using LLMs.

The demand for AI-powered data visualization tools is surging as businesses seek faster, more intuitive ways to understand their data. This project demonstrates how we can build our own AI-powered visualization tool that integrates seamlessly with existing data workflows.

## <u>🧠 **What This Project Does**</u>

VizAI understands natural language questions about your dataset and automatically:

Generates Python/Plotly visualization code using Groq LLM

Executes it on your uploaded CSV

Displays interactive charts

Provides insights

Supports SQL analytics

Exports PDF reports

## <u>🚀 **Features**</u>

💬 Natural language query interface for data visualization
📊 Support for multiple visualization types (line, bar, scatter, pie, bubble charts)
🧹 Automatic data preprocessing via Pandas
💻 Interactive Streamlit interface for easy data upload
⏳ Real-time visualization generation
🧠 Follow-up question support
🗄 SQL analytics mode
📄 PDF report generation
🔐 Basic authentication
📚 Chat history

## <u>🆕 **Models Used**</u>

→ Groq – Llama 3.3 70B (Primary)
→ Compatible with OpenAI / Gemini / Local Llama


This version is 100% free & local execution based.

## <u>🧱 **Project Structure**</u>

app.py — main Streamlit application

modules/ — helper modules

llm.py – prompt & Groq

e2b_runner.py – local executor

sql_engine.py – SQLite

history.py – memory

pdf_report.py – reports

auth.py – login

data/, img/, utils/ — assets

requirements.txt

## <u>⚙ **Prerequisites**</u>

Python 3.8+

pip or conda

Groq API Key

## <u>🛠 **Installation**</u>

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Create .env
GROQ_API_KEY=your_key

Run:
python -m streamlit run app.py

## <u>🧪 **How to Use**</u>

Upload CSV

Choose Mode

Natural Language

SQL

Ask questions like:

“Compare math marks of all students”
“Show sales by region”

SQL Example

SELECT name, attendance
FROM data
WHERE attendance > 90

## <u>🧩 **Technical Highlights**</u>

LLM → Plotly code generation

Safe execution on dataframe

Session-based multi-chart dashboard

Hybrid NL + SQL

PDF reporting without kaleido

Modular architecture

## <u>🧠 **Challenges Solved**</u>

LLM hallucination → forced df usage

Streamlit re-run → session state

Execution safety

Image export dependency

SQL table mapping

## <u>🚀 **Future Scope**</u>

DuckDB for large datasets

Role-based auth

Auto EDA

Voice queries

RAG over metadata

## <u>🤝 **Contributing**</u>

Open an issue or PR.

## <u>©️ **License**</u>

MIT License


