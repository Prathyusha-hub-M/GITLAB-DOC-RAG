import streamlit as st
import requests

API_URL = "http://localhost:8000/query"

st.set_page_config(
    page_title="GitLab Handbook RAG",
    page_icon="🤖",
)

st.sidebar.write("Model: Ollama")
st.sidebar.write("Embedding: SentenceTransformers")
st.sidebar.write("Vector DB: Chroma")
st.sidebar.write("Retriever: Hybrid BM25 + Vector")
st.sidebar.write("Framework: LangChain")

st.title("GitLab Handbook Assistant")
st.write("Ask questions about the GitLab handbook.")

# store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# chat input
prompt = st.chat_input("Ask a question about GitLab...")

if prompt:

    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # call FastAPI
    with st.spinner("Thinking..."):

        response = requests.post(
            API_URL,
            json={"query": prompt}
        )

        if response.status_code == 200:

            data = response.json()
            answer = data["answer"]
            sources = data["sources"]

        else:
            answer = "API request failed"
            sources = []

    # show assistant message
    with st.chat_message("assistant"):
        st.write(answer)

        if sources:
            with st.expander("Sources"):
                for src in sources:
                    st.write(src)

    st.session_state.messages.append({"role": "assistant", "content": answer})