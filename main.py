import streamlit as st
from config.aiservice import run_agent
from agent.tools.web_tools import web_tools
from langchain_core.messages import HumanMessage, AIMessageChunk
from utils.utils import format_output, format_tool_call
from config.prompt import PROMPT
import datetime
import asyncio

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    model_name = "gpt-4o-mini"
    agent, config, memory = run_agent(
        model_name=model_name,
        tools=web_tools,
        system_prompt=PROMPT.format(date=str(datetime.datetime.now().date()))
    )
    st.session_state.agent = agent
    st.session_state.config = config
    st.session_state.model_name = model_name

# Page config
st.set_page_config(page_title="Google Search Agent Asisstant", layout="wide")
st.title("Google Search Agent Asisstant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response
    with st.chat_message("assistant"):
        log_placeholder = st.empty()  # Placeholder for tools use
        message_placeholder = st.empty()  # Placeholder for message
        full_response = ""
        logs = []
        seen_logs = set()  # Track unique logs
        
        # Create input for agent
        input_data = {"messages": [HumanMessage(content=prompt)]}
        
        # Stream the response
        async def process_stream():
            response = ""
            resp = st.session_state.agent.astream(
                input=input_data, 
                config=st.session_state.config, 
                stream_mode=["messages", "updates"]
            )
            
            async for event, msg in resp:
                if event == "messages" and isinstance(msg[0], AIMessageChunk):
                    msg_chunk = format_output(msg[0], model_name=st.session_state.model_name)
                    response += msg_chunk
                    message_placeholder.markdown(response + "▌")
                
                elif event == "updates":
                    if "agent" in msg.keys() and not msg["agent"]["messages"][0].content:
                        ai_message_update_value = msg["agent"]["messages"][0]
                        log_data = format_tool_call(
                            ai_message_update_value,
                            st.session_state.model_name,
                        )
                        # Only add non-empty and unique logs
                        if log_data and str(log_data) not in seen_logs:
                            seen_logs.add(str(log_data))
                            logs.append(log_data)
                            # Update the log expander with all logs
                            with log_placeholder.expander("Tools Use", expanded=False):
                                for i, log in enumerate(logs):
                                    st.write(f"Step {i + 1}")
                                    st.json(log)
            return response

        # Run the async function
        full_response = asyncio.run(process_stream())
        
        # Update final response
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
