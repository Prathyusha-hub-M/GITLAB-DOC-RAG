from app.pipeline import run_rag_pipeline

query = "What is GitLab's incident escalation process?"

result = run_rag_pipeline(query)

print("\nAnswer:\n")
print(result["answer"])

print("\nSources:\n")
for src in result["sources"]:
    print("-", src)
