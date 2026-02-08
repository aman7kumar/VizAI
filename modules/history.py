# In-memory chat history
chat_history = []

def add_history(q, a):
    chat_history.append({
        "question": q,
        "answer": a
    })

def get_history():
    return chat_history


# Used by LLM for follow-up context
def get_context():
    context = ""
    for h in chat_history[-5:]:
        context += f"Q: {h['question']}\nA: {h['answer']}\n"
    return context
