from pandas import DataFrame
from streamlit import columns, expander, form, form_submit_button, fragment, sidebar, status, text_input, write, button, session_state
from Flashcards.display_flashcard import display_flashcard
from Audio.generate_audio import generate_audio_files

def display_flashcards(flashcards_df, sidebar_manager):
    """Display the flashcards in the app."""
    generate_audio_files(flashcards_df)  # Ensure all audio is pre-generated
    write("### Extracted Flashcards")
    
    # Sidebar to add a new flashcard
    session_state.flashcards_df = sidebar_manager.add_flashcard(session_state.flashcards_df)
    flashcards_df = session_state.flashcards_df

    # Pagination logic
    if "current_page" not in session_state:
        session_state.current_page = 0

    cards_per_page = 50
    total_pages = (len(flashcards_df) + cards_per_page - 1) // cards_per_page

    # Display page header
    col1, col2, col3 = columns(3 ,gap="large")
    col1.write(f"**`Number of flashcards: {len(flashcards_df)}`**")
    col2.write(f"**`Sort: {sidebar_manager.sort_option}`**")
    col3.write(f"**`Search: {sidebar_manager.search_query}`**")

    # Pagination controls
    with col1:
        if session_state.current_page > 0 and button("Previous"):
            session_state.current_page -= 1
    with col3:
        if session_state.current_page < total_pages - 1 and button("Next"):
            session_state.current_page += 1

    # Display current page number
    col2.write(f"**Page {session_state.current_page + 1} of {total_pages}**")

    # Subset data for the current page
    start_idx = session_state.current_page * cards_per_page
    end_idx = start_idx + cards_per_page
    page_flashcards_df = flashcards_df.iloc[start_idx:end_idx]

    num_columns = 5
    rows = [
        page_flashcards_df.iloc[i : i + num_columns]
        for i in range(0, len(page_flashcards_df), num_columns)
    ]

    with status("Loading", expanded=True):
        for row in rows:
            cols = columns(len(row))
            for col, (index, flashcard) in zip(cols, row.iterrows()):
                with col:
                    display_flashcard(flashcard)
