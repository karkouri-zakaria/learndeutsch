from pathlib import Path
from time import sleep
from streamlit import audio, button, columns, container, dataframe, expander, fragment, markdown, popover, rerun, session_state, slider, subheader, write
from Answers.answers import check_answer
from Audio_gen.generate_audio import generate_audio
from mutagen.mp3 import MP3
@fragment
def Quiz(flashcards_df):
    if 'flashcard_index' not in session_state:
        session_state.flashcard_index = 0
    if 'shuffled' not in session_state:
        session_state.shuffled = False
    if 'shuffle_enabled' not in session_state:
        session_state.shuffle_enabled = False
    if 'flashcards_df' not in session_state:
        session_state.flashcards_df = flashcards_df
    if 'original_flashcards_df' not in session_state and flashcards_df is not None:
        session_state.original_flashcards_df = flashcards_df.copy()
    if 'auto_continue' not in session_state:
        session_state.auto_continue = False
    if 'Show_all_anwsers' not in session_state:
        session_state.Show_all_anwsers = False
    if 'Results' not in session_state:
        session_state.Results = []
    if flashcards_df is not None:
        if not flashcards_df.empty:
            if session_state.shuffle_enabled and not session_state.shuffled:
                session_state.original_flashcards_df = flashcards_df.copy()
                session_state.flashcards_df = flashcards_df.sample(frac=1).reset_index(drop=True)
                session_state.flashcard_index = 0
                session_state.shuffled = True
            elif not session_state.shuffle_enabled and session_state.shuffled:
                session_state.flashcards_df = session_state.original_flashcards_df.copy()
                session_state.flashcard_index = 0
                session_state.shuffled = False
            flashcards_df = session_state.flashcards_df
            current_index = session_state.flashcard_index if session_state.flashcard_index < len(flashcards_df) else 0
            total_flashcards = len(flashcards_df)
            flashcard = flashcards_df.iloc[current_index]
            if total_flashcards > 1:
                new_index = slider(
                    "**Flashcard**", 
                    min_value=1, 
                    max_value=total_flashcards, 
                    value=current_index + 1,
                    format="%d"
                ) - 1
                if new_index != session_state.flashcard_index:
                    session_state.flashcard_index = new_index
                    rerun()
            else:
                session_state.current_index = 1
            with container(border=True):
                markdown(f"# {flashcard['English']}")
                left_button, right_button, _, correct, wrong, show_button = columns([1,1,1,1,1,2], gap="small")
                with left_button:
                    if button("⮜", key="prev_button", use_container_width=True, type="primary"):
                        session_state.flashcard_index = (current_index - 1) % total_flashcards
                        rerun()
                with right_button:
                    if button("⮞", key="next_button", use_container_width=True, type="primary"):
                        session_state.flashcard_index = (current_index + 1) % total_flashcards
                        write(session_state.flashcard_index)
                        if not any(result[1] == flashcard['English'] and result[3] in [True, False] for result in session_state.Results) and current_index <= len(session_state.Results) and not session_state.Show_all_anwsers:
                            session_state.Results = [result for result in session_state.Results if result[1] != flashcard['English']]
                            session_state.Results.append([int(current_index) + 1, flashcard['English'], flashcard['Deutsch'], None])
                        rerun()
                with correct:
                    if button("✅", key="correct_button", use_container_width=True, type="primary" if any(result[0] == flashcard['English'] and result[2] for result in session_state.Results) else "secondary"):
                        session_state.Results = [result for result in session_state.Results if result[1] != flashcard['English']]
                        session_state.Results.append([int(current_index)+1, flashcard['English'], flashcard['Deutsch'], True])
                        session_state.flashcard_index = (current_index + 1) % total_flashcards
                        rerun()
                with wrong:
                    if button("❌", key="wrong_button", use_container_width=True, type="primary" if any(result[0] == flashcard['English'] and not result[2] for result in session_state.Results) else "secondary"):
                        session_state.Results = [result for result in session_state.Results if result[1] != flashcard['English']]
                        session_state.Results.append([int(current_index)+1, flashcard['English'], flashcard['Deutsch'], False])
                        session_state.flashcard_index = (current_index + 1) % total_flashcards
                        rerun()
                if session_state.Show_all_anwsers:
                    markdown(f"# {flashcard['Deutsch']}")
                    try:
                        audio_path = Path(f"cached_audios/{flashcard['Deutsch']}.mp3")
                        if not audio_path.exists():
                            audio_path = generate_audio(flashcard["Deutsch"])
                        with open(audio_path, "rb") as audio_file:
                            audio(audio_file, format="audio/mp3", autoplay=True)
                        if session_state.auto_continue:
                            sleep(MP3(audio_path).info.length * 3)
                            session_state.flashcard_index = (current_index + 1) % total_flashcards
                            rerun()
                    except Exception as e:
                        write(f"Error generating audio: {str(e)}")
                else:
                    check_answer(flashcard, current_index, total_flashcards)
                    with show_button:
                        with popover("Answer", use_container_width=True):
                            markdown(f"# {flashcard['Deutsch']}")
                            col1, col2 = columns([6, 3])
                            try:
                                audio_path = Path(f"cached_audios/{flashcard['Deutsch']}.mp3")
                                if not audio_path.exists():
                                    audio_path = generate_audio(flashcard["Deutsch"])
                                with open(audio_path, "rb") as audio_file:
                                    col1.audio(audio_file, format="audio/mp3", autoplay=False)
                            except Exception as e:
                                write(f"Error generating audio: {str(e)}")
                            link = f"https://www.verbformen.com/?w={flashcard['Deutsch']}"
                            col2.markdown(f"""<a href="{link}" target="_blank" style="text-decoration: none;"><button style="padding: 10px; background-color: #ffc107; color: white; border: none; border-radius: 30px; cursor: pointer;">📖 Wörterbuch</button></a>""", unsafe_allow_html=True)
            if not session_state.Show_all_anwsers:
                with expander(
                    f"👍🏼 Correct ({sum(r[3] == True for r in session_state.Results) / (l := len(session_state.Results) or 1) * 100:.1f}%)"
                    f" - 👎🏼 Wrong ({sum(r[3] == False for r in session_state.Results) / l * 100:.1f}%)"
                    f" - 👉🏼 Skipped ({sum(r[3] is None for r in session_state.Results) / l * 100:.1f}%) ",
                ):
                    subheader("Wrong Answers")
                    dataframe([{'English : deutsch': f"{r[0]} - {r[1]} : {r[2]}"} for r in session_state.Results if r[3] == False], hide_index=True, use_container_width=True)
                    subheader("Skipped Answers")
                    dataframe([{'English : deutsch': f"{r[0]} - {r[1]} : {r[2]}"} for r in session_state.Results if r[3] is None], hide_index=True, use_container_width=True)
        else:
            _, message_col, _ = columns([1, 2, 1], gap="small")
            with message_col:
                markdown("### ⚠️ No flashcards available. Please upload a valid file.")