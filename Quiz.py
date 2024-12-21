from streamlit import audio, button, columns, container, expander, fragment, metric, popover, session_state, markdown, write
from pathlib import Path
from Audio.generate_audio import generate_audio

@fragment
def Quiz(flashcards_df):

    if flashcards_df is not None:
        if not flashcards_df.empty:
            # Shuffle flashcards once and store in session state
            if "shuffled_flashcards" not in session_state:
                session_state.shuffled_flashcards = flashcards_df.sample(frac=1).reset_index(drop=True)
                session_state.flashcard_index = 0  # Initialize index after shuffling

            # Access shuffled flashcards
            shuffled_flashcards = session_state.shuffled_flashcards

            # Get the current flashcard
            current_index = session_state.flashcard_index
            total_flashcards = len(shuffled_flashcards)     
            flashcard = shuffled_flashcards.iloc[current_index]

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
