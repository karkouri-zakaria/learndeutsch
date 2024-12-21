from pandas import DataFrame
from streamlit import columns, expander, form, form_submit_button, fragment, markdown, metric, sidebar, status, text_input, write, button, session_state
from Flashcards.display_flashcard import display_flashcard
from Audio.generate_audio import generate_audio_files

def display_flashcards(flashcards_df, sidebar_manager):
    """Display the flashcards in the app."""

    col1, col2, col3 = columns([4,1,6] ,gap="small", vertical_alignment="bottom")

    col1.header("Extracted Flashcards")
    
    # Sidebar to add a new flashcard
    session_state.flashcards_df = sidebar_manager.add_flashcard(session_state.flashcards_df)

    # Pagination logic
    if "current_page" not in session_state:
        session_state.current_page = 0

    cards_per_page = 100
    total_pages = (len(flashcards_df) + cards_per_page - 1) // cards_per_page

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
    if sidebar_manager.search_query:
        col3.markdown(f"`{sidebar_manager.sort_option}`")
    else:
        col3.markdown("↕️ No Sort applied")

    # Pagination controls
    write("---")
    colpg, colp, coln = columns(3 ,gap="large")
    with colp:
        if session_state.current_page > 0 and button("Previous", use_container_width=True):
            session_state.current_page -= 1
    with coln:
        if session_state.current_page < total_pages - 1 and button("Next", use_container_width=True):
            session_state.current_page += 1

    # Display current page number
    colpg.metric(f"Page", f"{session_state.current_page + 1} of {total_pages}")

    # Subset data for the current page
    start_idx = session_state.current_page * cards_per_page
    end_idx = start_idx + cards_per_page
    page_flashcards_df = flashcards_df.iloc[start_idx:end_idx]
    generate_audio_files(page_flashcards_df)  # Ensure all audio is pre-generated


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
                    display_flashcard(index, flashcard)
