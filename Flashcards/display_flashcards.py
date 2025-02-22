from streamlit import columns, markdown, metric, session_state, slider, status, write
from Flashcards.display_flashcard import display_flashcard
from Audio.generate_audio import generate_audio_files

def display_flashcards(flashcards_df, num_columns=1, cards_per_page=20):
    """Display the flashcards in the app."""
    
    # Pagination logic
    if "current_page" not in session_state:
        session_state.current_page = 0
    
    # Handle empty DataFrame
    if len(flashcards_df) == 0:
        metric("Number of Flashcards", "0")
        markdown("🔍 No flashcards to display")
        write("No flashcards match the current criteria.")
        return  # Exit the function early if no data to display

    total_pages = max(1, (len(flashcards_df) + cards_per_page - 1) // cards_per_page)

    # Display the number of flashcards
    metric("Number of Flashcards", f"{len(flashcards_df)}")

    # Pagination controls
    if total_pages > 1:
        session_state.current_page = slider(
            "Select Page", 
            min_value=0, 
            max_value=total_pages - 1, 
            value=session_state.current_page,
            format="Page %d"
        )
    else:
        session_state.current_page = 0

    # Subset data for the current page
    start_idx = session_state.current_page * cards_per_page
    end_idx = start_idx + cards_per_page
    page_flashcards_df = flashcards_df.iloc[start_idx:end_idx]
    generate_audio_files(page_flashcards_df)  # Ensure all audio is pre-generated

    rows = [
        page_flashcards_df.iloc[i : i + num_columns]
        for i in range(0, len(page_flashcards_df), num_columns)
    ]

    with status("Loading", expanded=True):
        for row in rows:
            cols = columns(len(row))
            for col, (index, flashcard) in zip(cols, row.iterrows()):
                with col:
                    display_flashcard(index, flashcard)
