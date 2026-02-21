import json
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import _faithfulness, _answer_relevancy, _context_precision

from langchain_community.chat_models import ChatHuggingFace
from langchain_community.llms import HuggingFaceHub

from app.pipeline import run_rag_pipeline

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

llm = HuggingFaceHub(repo_id="HuggingFaceH4/zephyr-7b-beta",
                          model_kwargs={"temperature":0})
    
evaluator_llm = ChatHuggingFace(llm=llm)

results = evaluate(
        dataset,
        metrics=[
            _faithfulness,
            _answer_relevancy,
            _context_precision
        ],
        llm= evaluator_llm
    )


print("\nRAGAS Evaluation Results:\n")
print(results)

