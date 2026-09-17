# AI Support Agent & LLM-as-a-Judge Evaluation Framework

An end-to-end AI customer support agent equipped with an automated LLM-as-a-Judge evaluation framework built on golden test datasets.

# Project Structure
```
hiver-ai-support-agent/
├── data/
│   ├── dataset.json
│   └── golden_set.json
├── src/
│   ├── agent.py
│   └── evaluator.py
├── .env
├── requirements.txt
├── README.md
└── REPORT.md
```

## Quickstart

1. **Clone Repo & Install Dependencies**
```bash
git clone <your-repo-link>
cd hiver-ai-support-agent
pip install -r requirements.txt
```
2. **Configure Environment Variables**
Create a .env file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```
3. **Run the AI Support Agent**
```
python src/agent.py
```

4. **Run the LLM-as-a-Judge Evaluation**
```
python src/evaluator.py`
```
