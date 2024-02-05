import streamlit as st
import random
import time
import replicate
import os
# Set Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "r8_9TQIIw4x4IrdtXpexi6uTOWseI4lXUP2aNJjl"


# Prompts
pre_prompt = "As a mental health assistant, I am here to provide support and guidance for any mental health concerns or questions you may have. Please feel free to share what's on your mind."

st.title("Welly ChatBot 🧑🏽‍⚕️")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input(""):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
                           input={"prompt": f"{pre_prompt} {prompt} Assistant:",
                                  "temperature": 0.1, "top_p": 0.9, "max_length": 512, "repetition_penalty": 1})
        
        
        # Simulate stream of response with milliseconds delay
        full_response=""
        count=0
        if output !="":
            count+=1
        for item in output:
            full_response += item + " "
            time.sleep(0.05)
            if count >=1:
                assistant_response = full_response[0].replace("Hello!", "").strip()
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
