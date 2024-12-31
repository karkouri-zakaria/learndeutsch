from pathlib import Path
from streamlit import audio, button, columns, container, fragment, markdown, metric, popover, session_state, text_input, toggle, write
from Audio.generate_audio import generate_audio

from streamlit import markdown, text_input, button

@fragment
def check_answer(flashcard, current_index):
    """Check the user's answer and provide feedback highlighting only mistakes."""
    
    # Input and feedback for the answer
    answer = text_input(
        "Type your answer in Deutsch:",
        key=f"answer_input_{current_index}",
    )
    submit = button(
        "Submit",
        key=f"submit_button_{current_index}",
        type="primary",
        help="Check your answer",
        use_container_width=True,
    )

    # Display feedback only when "Submit" is clicked
    if submit:
        correct_answer = flashcard['Deustch'].strip().lower()
        user_answer = answer.strip().lower()

        # Perform character-by-character comparison
        feedback = ""
        mistakes_found = False  # Flag to check if there are mistakes

        # Compare up to the length of the user's answer
        for i, user_char in enumerate(user_answer):
            if i < len(correct_answer) and user_char == correct_answer[i]:
                feedback += f"<span style='color: green;'>{user_char}</span>"
            else:
                feedback += f"<span style='color: red;'>{user_char}</span>"
                mistakes_found = True

        # Mark extra characters in the user's answer beyond the length of the correct answer
        if len(user_answer) > len(correct_answer):
            for extra_char in user_answer[len(correct_answer):]:
                feedback += f"<span style='color: red;'>{extra_char}</span>"
                mistakes_found = True

        # Provide feedback
        if mistakes_found:
            markdown(
                f"❌ **Try again.** Here's your input with mistakes highlighted:<br>{feedback}",
                unsafe_allow_html=True,
            )
        else:
            markdown("✅ **Correct!** Great job!")


@fragment
def Quiz(flashcards_df):
    if 'flashcard_index' not in session_state:
        session_state.flashcard_index = 0
    if 'shuffled' not in session_state:
        session_state.shuffled = False  # Track shuffle state
    if 'flashcards_df' not in session_state:
        session_state.flashcards_df = flashcards_df  # Store the original order

    if flashcards_df is not None:
        if not flashcards_df.empty:
            # Check the shuffle toggle
            shuffle_enabled = toggle(
                "Shuffle flashcards", 
                key="shuffle_flashcards", 
                value=session_state.shuffled, 
                help="Randomize the flashcards order"
            )

            # Shuffle or reset flashcards based on toggle state
            if shuffle_enabled and not session_state.shuffled:
                session_state.flashcards_df = flashcards_df.sample(frac=1).reset_index(drop=True)
                session_state.flashcard_index = 0  # Reset to first flashcard
                session_state.shuffled = True
            elif not shuffle_enabled and session_state.shuffled:
                session_state.flashcards_df = flashcards_df  # Restore original order
                session_state.flashcard_index = 0  # Reset to first flashcard
                session_state.shuffled = False

            # Access the current flashcards data
            flashcards_df = session_state.flashcards_df

            # Get the current flashcard
            current_index = session_state.flashcard_index
            total_flashcards = len(flashcards_df)
            flashcard = flashcards_df.iloc[current_index]

            # Display the flashcard content
            with container(border=True):
                metric("Flashcard", f"{current_index + 1} of {total_flashcards}")

                # Horizontal Buttons
                left_button, right_button, _ = columns([1, 1, 10])  # Create space for buttons
                with left_button:
                    if button("⮜", key="prev_button", use_container_width=True, type="primary", help="Previous flashcard"):
                        session_state.flashcard_index = (current_index - 1) % total_flashcards
                with right_button:
                    if button("⮞", key="next_button", use_container_width=True, type="primary", help="Next flashcard"):
                        session_state.flashcard_index = (current_index + 1) % total_flashcards
                markdown(f"# {flashcard['English']}")

                # Expander for Answer
                with popover("**Deutsch:**", icon="💡", use_container_width=True, help="Click to open"):
                    markdown(f"# {flashcard['Deustch']}")

                    # Generate or load cached audio
                    try:
                        audio_path = Path(f"cached_audios/{flashcard['Deustch']}.mp3")
                        if not audio_path.exists():
                            audio_path = generate_audio(flashcard["Deustch"])  # Replace with your actual audio generation logic
                        with open(audio_path, "rb") as audio_file:
                            audio(audio_file, format="audio/mp3", autoplay=False)
                    except Exception as e:
                        write(f"Error generating audio: {str(e)}")

                # Call the answer-checking feature
                check_answer(flashcard, current_index)
        else:
            _, message_col, _ = columns([1, 2, 1])  # Center the no flashcards message
            with message_col:
                markdown("### ⚠️ No flashcards available. Please upload a valid file.")
