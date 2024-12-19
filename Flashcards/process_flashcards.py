def process_flashcards(flashcards_df, sidebar_manager):
    """Filter, sort, and display flashcards based on user input."""
    if sidebar_manager.search_query:
        flashcards_df = flashcards_df[
            flashcards_df["FrontText"].str.contains(
                sidebar_manager.search_query, case=False, na=False
            )
            | flashcards_df["BackText"].str.contains(
                sidebar_manager.search_query, case=False, na=False
            )
        ]

    if sidebar_manager.sort_option == "Front Text":
        flashcards_df = flashcards_df.sort_values(by="FrontText").reset_index(drop=True)
    elif sidebar_manager.sort_option == "Back Text":
        flashcards_df = flashcards_df.sort_values(by="BackText").reset_index(drop=True)
    elif sidebar_manager.sort_option == "Shuffle":
        flashcards_df = flashcards_df.sample(frac=1).reset_index(drop=True)

    return flashcards_df