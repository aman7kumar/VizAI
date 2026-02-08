import os
from groq import Groq
from modules.history import get_context

def generate_code(user_query, columns):
    """
    Convert natural language query into Python visualization code using Groq LLM
    with conversation memory support.
    """

    prompt = f"""
    You are a data visualization expert.

    Previous conversation context:
    {get_context()}

    IMPORTANT RULES:
    1. A pandas dataframe named df already exists – USE IT.
    2. DO NOT create a new dataframe.
    3. Create a Plotly figure stored in variable named fig.
    4. DO NOT call fig.show()
    5. Return ONLY Python code, nothing else.
    6. You may also create a variable named insight containing text summary.

    Available columns: {columns}

    User request: {user_query}
    """

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    # -------- CLEAN MARKDOWN --------
    code = response.choices[0].message.content

    code = code.replace("```python", "")
    code = code.replace("```", "")
    code = code.strip()

    return code
