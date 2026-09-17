import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_kb():
    with open("data/dataset.json", "r") as f:
        return json.load(f)

def run_support_agent(user_query: str) -> str:
    kb_data = load_kb()
    context = "\n".join([f"- Issue: {item['issue']} | Solution: {item['solution']}" for item in kb_data])
    
    prompt = f"""
    You are an AI Customer Support Agent for an enterprise platform.
    Use the following Knowledge Base context to answer customer questions accurately, politely, and concisely.
    If the request is out of scope or unreasonable, remain professional and state that it needs human escalation.

    Context:
    {context}

    Customer Query: {user_query}
    Agent Response:
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    test_query = "I was double charged today"
    print(f"Query: {test_query}\nResponse: {run_support_agent(test_query)}")
