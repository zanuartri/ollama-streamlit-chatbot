import subprocess
from langchain_ollama import OllamaLLM
import streamlit as st

# ------------------------
# Function to get available models from Ollama
# ------------------------
def get_available_models():
    result = subprocess.run(["ollama", "list"], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().split("\n")
    models = []
    for line in lines[1:]:  # skip header
        model_name = line.split()[0]
        models.append(model_name)
    return models

# ------------------------
# Streamlit UI setup
# ------------------------

st.title("AI Chatbot with Auto-detected Ollama Models")

# Fetch models dynamically
available_models = get_available_models()

if available_models:
    # Model selection UI
    selected_model = st.selectbox("Select a model:", available_models)

    # Initialize selected model
    llm = OllamaLLM(model=selected_model)

    # ------------------------
    # Chat UI logic
    # ------------------------

    st.write("Ask your questions below.")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input handling
    if prompt := st.chat_input("Your question:"):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Query LLM directly (no memory, no RAG)
        response = llm.invoke(prompt)

        # Display assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

else:
    st.error("No models detected. Please pull models using `ollama pull <model>`.")