from pathlib import Path

from streamlit import audio, button, columns, container, fragment, markdown, metric, popover, session_state, toggle, write
from Audio.generate_audio import generate_audio

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
                markdown(f"# {flashcard['FrontText']}")

                # Expander for Answer
                with popover("**Deutsch:**", icon="💡", use_container_width=True, help="Click to open"):
                    markdown(f"# {flashcard['BackText']}")

                    # Generate or load cached audio
                    try:
                        audio_path = Path(f"cached_audios/{flashcard['BackText']}.mp3")
                        if not audio_path.exists():
                            audio_path = generate_audio(flashcard["BackText"])  # Replace with your actual audio generation logic
                        with open(audio_path, "rb") as audio_file:
                            audio(audio_file, format="audio/mp3", autoplay=False)
                    except Exception as e:
                        write(f"Error generating audio: {str(e)}")
        else:
            _, message_col, _ = columns([1, 2, 1])  # Center the no flashcards message
            with message_col:
                markdown("### ⚠️ No flashcards available. Please upload a valid file.")