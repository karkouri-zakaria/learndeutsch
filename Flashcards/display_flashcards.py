from streamlit import columns, session_state, slider, status, write
from Flashcards.display_flashcard import display_flashcard
from Audio.generate_audio import generate_audio_files

def display_flashcards(flashcards_df, sidebar_manager, num_columns=4):
    """Display the flashcards in the app."""

    col1, col2, col3 = columns([4, 1, 6], gap="small", vertical_alignment="bottom")

    col1.header("Extracted Flashcards")
    
    # Sidebar to add a new flashcard
    session_state.flashcards_df = sidebar_manager.add_flashcard(session_state.flashcards_df)

    # Pagination logic
    if "current_page" not in session_state:
        session_state.current_page = 0

    cards_per_page = 100

    # Handle empty DataFrame
    if len(flashcards_df) == 0:
        col1.metric("Number of Flashcards", "0")
        col3.markdown("🔍 No flashcards to display")
        write("No flashcards match the current criteria.")
        return  # Exit the function early if no data to display

    total_pages = max(1, (len(flashcards_df) + cards_per_page - 1) // cards_per_page)

    # Display the number of flashcards
    col1.metric("Number of Flashcards", f"{len(flashcards_df)}")

    # Display the search query
    col2.markdown("Search:")
    if sidebar_manager.search_query:
        col3.markdown(f"`{sidebar_manager.search_query}`")
    else:
        col3.markdown("🔍 No search applied")

    # Display the selected sort option
    col2.markdown("Sort by:")
    if sidebar_manager.sort_option:
        col3.markdown(f"`{sidebar_manager.sort_option}`")
    else:
        col3.markdown("↕️ No Sort applied")

    # Pagination controls
    write("---")
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
