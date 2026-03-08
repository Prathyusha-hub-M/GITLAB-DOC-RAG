import json
from datasets import Dataset
from dotenv import load_dotenv

from ragas import evaluate
from ragas.metrics import _faithfulness, _answer_relevancy, _context_precision

from langchain_openai import ChatOpenAI

from app.pipeline import run_rag_pipeline

load_dotenv()

with open("data/ragas_eval.json", "r") as f:
    questions = json.load(f)

records =[]

for item in questions:
        query = item["question"]

        result = run_rag_pipeline(query)

        records.append({
            "question":query,
            "answer":result["answer"],
            "contexts":result["contexts"],
        })

dataset = Dataset.from_list(records)

llm = ChatOpenAI(
      model="gpt-4o-mini",
      temperature = 0
      )


results = evaluate(
        dataset,
        metrics=[
            _faithfulness,
            _answer_relevancy,
            _context_precision
        ],
        llm=llm
    )


print("\nRAGAS Evaluation Results:\n")
print(results)

