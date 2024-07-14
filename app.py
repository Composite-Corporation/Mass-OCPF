import streamlit as st
from pydantic import Field, BaseModel
from typing import Optional, List
from text2sql import Text2SQL

# Basic page config and UI setup
st.set_page_config(page_title="Composite.ai", page_icon="♻️")
st.image("assets/logo-full.png", output_format="PNG", width=300)
st.markdown(
    body="""
    <style>
        .katex .base {
            color: orange;
            font-size: 14px;
        }
    </style>
    """, 
    unsafe_allow_html=True,
)

# Instantiating copilot agent and cache so not rereun
@st.cache_resource
def load_agent():
    return Text2SQL()

agent = load_agent()

# Class for storing chat message data
class Chat(BaseModel):
    name: str = Field(description="Name of the chat message sender, e.g. 'user' or 'assistant'")
    content: str = Field(description="Content of the chat message")
    info: Optional[List[str]] = Field(description="Additional supporting infomation to be displayed in expander", default=None)

# Helper function to create chat bubble widgets
def chat_bubble(chat: Chat):
    name = chat.name
    if name == "user":
        avatar = "👨‍💻"
    else:
        avatar="🤖"
    with st.chat_message(name=name, avatar=avatar):
        with st.container(border=True):
            st.markdown(chat.content)
        if chat.info:
            with st.expander(label="Intermediate Steps", expanded=False) as expander:
                for item in chat.info:
                    with st.container(border=True):
                        st.markdown(item)

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [
        Chat(name="assistant", content="Hi! I'm an AI chat bot for the Massachusetts OCPF. Can I help you answer any questions about our public documents?"),
    ]

# Display chat history using st.chat_message
for chat in st.session_state['chat_history']:
    chat_bubble(chat=chat)

# User input
if user_input := st.chat_input(placeholder="Ask any question here"):
    # Create and display user chat object, then add to history
    user_chat = Chat(name="user", content=user_input)
    chat_bubble(chat=user_chat)
    st.session_state['chat_history'].append(user_chat)
    
    # Process AI response and display intermediate steps
    intermediate_steps = []
    with st.chat_message(name="assistant", avatar="🤖"):
        with st.status("AI Processing...", expanded=True) as status:
            response_object = agent.converse(user_input=user_input)
            intermediate_steps.append(f"Generated SQL Query:\n\n```sql\n{response_object.query}\n```")
            intermediate_steps.append(f"Query Results:\n\n```json\n{response_object.results}\n```")

    # Add AI response to chat history
    ai_chat = Chat(name="assistant", content=response_object.response, info=intermediate_steps)
    st.session_state['chat_history'].append(ai_chat)

    # Re-render page to display update chat history
    st.rerun()
    
