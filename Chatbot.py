from streamlit import fragment, session_state, sidebar, spinner, write, chat_input, chat_message, button
from threading import Thread
from queue import Queue

@fragment
def Chatbot(bot):

    # Function to fetch response (moved above its usage)
    def fetch_response(bot, conversation_history, result_queue):
        response = bot.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=conversation_history,
            max_tokens=100,
        )
        result_queue.put(response)

    # Queue to hold the result of the background thread
    result_queue = Queue()

    # Define the system message
    system_message = {
        "role": "system",
        "content": (
           "You are Qwen, a concise, professional English assistant with expertise in teaching German, providing clear explanations, translations, and examples in ten words or fewer as you main task and priority. Prioritize brevity and make reasonable assumptions for helpful, direct answers."
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

            # Generate and display assistant's response
            assistant_response = ""  # Accumulate the assistant's response
            try:
                # Start background thread for response generation
                thread = Thread(target=fetch_response, args=(bot, session_state.messages, result_queue))
                thread.start()

                with chat_message("assistant"):
                    with spinner("Thinking..."):
                        thread.join()  # Wait for the thread to finish
                        response = result_queue.get()
                        assistant_response = response["choices"][0]["message"]["content"]
                        write(assistant_response)

                # Append the full assistant response to session state
                session_state.messages.append(
                    {"role": "assistant", "content": assistant_response}
                )

            except Exception as e:
                # Handle errors gracefully
                with chat_message("assistant"):
                    write(f"Error: {e}")