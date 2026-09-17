import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from agent import run_support_agent

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_response(query: str, ground_truth: str, model_response: str) -> dict:
    judge_prompt = f"""
    You are an expert LLM Evaluator for Customer Support Quality.
    Evaluate the model response against the ground truth based on:
    1. Correctness (0-10)
    2. Tone/Empathy (0-10)
    3. Hallucination Risk (High/Medium/Low)

    Query: {query}
    Ground Truth: {ground_truth}
    Model Response: {model_response}

    Return JSON strictly in this format:
    {{
        "correctness": score,
        "tone": score,
        "hallucination": "Low/Medium/High",
        "reasoning": "Brief explanation"
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0.0
    )
    return json.loads(response.choices[0].message.content)

def run_evals():
    with open("data/golden_set.json", "r") as f:
        golden_set = json.load(f)
    
    results = []
    for test in golden_set:
        agent_out = run_support_agent(test["customer_query"])
        eval_metrics = evaluate_response(test["customer_query"], test["ground_truth"], agent_out)
        
        results.append({
            "id": test["query_id"],
            "query": test["customer_query"],
            "agent_response": agent_out,
            "eval": eval_metrics
        })
        print(f"Evaluated {test['query_id']} | Correctness: {eval_metrics['correctness']}/10")
        
    with open("eval_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_evals()
