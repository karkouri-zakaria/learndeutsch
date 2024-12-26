from streamlit import fragment, session_state, sidebar, spinner, write, chat_input, chat_message, button


@fragment
def Chatbot(bot):

    # Define the system message
    system_message = {
        "role": "system",
        "content": (
            "You are Qwen. You speak mainly English, you are a helpful, concise, and professional English assistant with expertise in teaching "
            "the German language. When addressing questions about German, you provide clear and accurate explanations, "
            "translations, and illustrative example sentences. Your responses should prioritize brevity, focusing only "
            "on the most relevant details in ten words or fewer. If additional clarification is needed, offer succinct "
            "follow-ups, but do not ask questions about context. Instead, make reasonable assumptions to deliver the most helpful "
            "and direct answer. Your responses can seamlessly switch between English and German as required by the context or as "
            "preferred by the user."
        ),
    }

    # Initialize session state for messages
    if "messages" not in session_state:
        session_state.messages = [system_message]

    # Initialize the state for chat visibility
    if "show_chat" not in session_state:
        session_state.show_chat = False

    # Function to toggle chat visibility and reset context if closed
    def toggle_chat():
        session_state.show_chat = not session_state.show_chat
        if not session_state.show_chat:
            session_state.messages = [system_message]  # Reset messages with system message

    # Sidebar button to toggle the chat
    write("---")
    button("Chatbot", on_click=toggle_chat, icon="💬", use_container_width=True)

    # Popover for Chat Interface
    if session_state.show_chat:
            # Display previous messages in chat
            for message in session_state.messages[1:]:  # Skip the system message for display
                with chat_message(message["role"]):
                    write(message["content"])

            # User prompt input
            if prompt := chat_input("Ask a question:"):
                # Append user's message to session state
                session_state.messages.append({"role": "user", "content": prompt})
                with chat_message("user"):
                    write(prompt)

                # Function to generate LLM response
                def generate_response(conversation_history):
                    return bot.chat.completions.create(
                        model="Qwen/Qwen2.5-72B-Instruct",
                        messages=conversation_history,
                        max_tokens=500,
                        stream=True,
                    )

                # Generate and display assistant's response
                assistant_response = ""  # Accumulate the assistant's response
                try:
                    with chat_message("assistant"):
                        with spinner("Thinking..."):
                            # Include the entire conversation history in the API call
                            for chunk in generate_response(session_state.messages):
                                if "choices" in chunk and len(chunk.choices) > 0:
                                    content = chunk.choices[0].delta.get("content", "")
                                    assistant_response += content
                        write(assistant_response)

                    # Append the full assistant response to session state
                    session_state.messages.append(
                        {"role": "assistant", "content": assistant_response}
                    )

                except Exception as e:
                    # Handle errors gracefully
                    with chat_message("assistant"):
                        write(f"Error: {e}")