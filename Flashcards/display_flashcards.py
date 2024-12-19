from streamlit import columns, fragment, status, write
from Flashcards.display_flashcard import display_flashcard

@fragment
def display_flashcards(flashcards_df, sidebar_manager):
    """Display the flashcards in the app."""
    write("### Extracted Flashcards")

    col1, col2, col3 = columns(3)
    col1.write(f"Number of flashcards: {len(flashcards_df)}")
    col2.write(f"Sort: {sidebar_manager.sort_option}")
    col3.write(f"Search: {sidebar_manager.search_query}")

    num_columns = 5
    rows = [
        flashcards_df.iloc[i : i + num_columns]
        for i in range(0, len(flashcards_df), num_columns)
    ]

    with status("**Loading**", expanded=True):
        for row in rows:
            cols = columns(len(row))
            for col, (index, flashcard) in zip(cols, row.iterrows()):
                with col:
                    display_flashcard(flashcard)