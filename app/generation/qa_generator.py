from typing import List, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langsmith import traceable
from tenacity import retry, stop_after_attempt, wait_exponential


class QAGenerator:
    def __init__(
        self,
        llm: BaseChatModel,
        max_context_chars: int = 8000,
    ):
        """
        Args:
            llm: Any LangChain-compatible chat model (Grok, OpenAI, Ollama, etc.)
            max_context_chars: Safety limit to prevent context overflow
        """
        self.llm = llm
        self.max_context_chars = max_context_chars

    def _truncate_context(self, context_block: str) -> str:
        """Basic character-based truncation to prevent overflow."""
        return context_block[: self.max_context_chars]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def _safe_invoke(self, messages):
        """Retry wrapper for robustness."""
        return self.llm.invoke(messages)
    
    #Generation

    @traceable(name="llm_generate")
    def generate(self, query: str, contexts: List[Dict]) -> Dict:
        """
        Generates answer using retrieved contexts.

        Returns structured output compatible with:
        - LangSmith tracing
        - RAGAS evaluation
        - API response layer
        """

        # Merge context safely
        context_block = "\n\n".join(
            r.get("text", "") for r in contexts
        )
        context_block = self._truncate_context(context_block)

        # Extract sources defensively
        sources = [
            r.get("metadata", {}).get("file_path", "unknown")
            for r in contexts
        ]

        messages = [
            SystemMessage(
                content=(
                    "You must answer ONLY using the provided context. "
                    "If the answer is not present in the context, say you do not know."
                )
            ),
            HumanMessage(
                content=f"Context:\n{context_block}\n\nQuestion:\n{query}"
            ),
        ]

        # Invoke model safely
        response = self._safe_invoke(messages)

        return {
            "answer": response.content,
            "sources": sources,
            "contexts": [
                {
                    "text": r.get("text", ""),
                    "source": r.get("metadata", {}).get("file_path", "unknown"),
                }
                for r in contexts
            ],
        }

    
