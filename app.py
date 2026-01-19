import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
import tempfile
# 1. Load your secret keys
load_dotenv()

# 2. Setup the Page Design
st.set_page_config(page_title="AI Travel Agent", page_icon="✈️")
st.title("✈️ Global Travel Agent")
st.markdown("---")

# 3. Create a Sidebar for Settings
st.sidebar.title("🤖 Agent Settings")
model_choice = st.sidebar.selectbox(
    "Select AI Brain:",
    ["Gemini 3 Flash (Fast)", "GPT-5.2 (High Reasoning)"]
)

# 4. Initialize the chosen AI model
if model_choice == "Gemini 3 Flash (Fast)":
    # Gemini 3 is the newest model with a native 'thinking' mode
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview", 
        thinking_level="high" # Makes it better at logic
    )
else:
    # GPT-5.2 for complex reasoning
    llm = ChatOpenAI(model="gpt-5.2")

# 5. Build the Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Logic when you type a message
if prompt := st.chat_input("Ask about your trip (e.g. 'Do I need a visa for Singapore?')"):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show "Thinking" spinner
    with st.spinner(f"{model_choice} is thinking..."):
        try:
            response = llm.invoke(prompt)
            full_response = response.content
            
            # Show AI response
            with st.chat_message("assistant"):
                st.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {e}. Check if your API keys are correct in the .env file!")