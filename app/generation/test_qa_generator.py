import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from app.generation.qa_generator import QAGenerator

load_dotenv()


def main():
    # Make sure Ollama is running locally:
    # ollama run llama3

    llm = ChatOllama(
        model="llama3",
        temperature=0,
    )

    generator = QAGenerator(llm=llm)

    test_contexts = [
        {
            "text": "GitLab is a DevOps platform that supports CI/CD.",
            "metadata": {"file_path": "docs/ci.md"},
        },
        {
            "text": "GitLab provides version control and issue tracking.",
            "metadata": {"file_path": "docs/version_control.md"},
        },
    ]

    result = generator.generate(
        query="What is GitLab used for?",
        contexts=test_contexts,
    )

    print("\nAnswer:\n", result["answer"])
    print("\nSources:\n", result["sources"])


if __name__ == "__main__":
    main()