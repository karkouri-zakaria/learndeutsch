from pathlib import Path
from time import sleep
from streamlit import audio, button, columns, container, dataframe, expander, fragment, markdown, popover, rerun, session_state, slider, subheader, write
from Answers.answers import check_answer, save_results
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
    if 'show_wrongs' not in session_state:
        session_state.show_wrongs = False
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
                left_button, right_button, correct, wrong, show_button = columns([1,1,1,1,3], gap="small")
                with left_button:
                    if button("⮜", key="prev_button", use_container_width=True, type="primary"):
                        session_state.flashcard_index = (current_index - 1) % total_flashcards
                        rerun()
                with right_button:
                    if button("⮞", key="next_button", use_container_width=True, type="primary"):
                        session_state.flashcard_index = (current_index + 1) % total_flashcards
                        write(session_state.flashcard_index)
                        rerun()
                with correct:
                    if button("✅", key="correct_button", use_container_width=True, type="primary" if any(result[0] == flashcard['English'] and result[2] for result in session_state.Results) else "secondary") and not session_state.show_wrongs:
                        session_state.Results = [result for result in session_state.Results if result[1] != flashcard['English']]
                        session_state.Results.append([int(current_index)+1, flashcard['English'], flashcard['Deutsch'], True])
                        session_state.flashcard_index = (current_index + 1) % total_flashcards
                        audio_path = Path(f"cached_audios/{flashcard['Deutsch']}.mp3")
                        if not audio_path.exists():
                            audio_path = generate_audio(flashcard["Deutsch"])
                        with open(audio_path, "rb") as audio_file:
                            audio(audio_file, format="audio/mp3", autoplay=True)
                        sleep(MP3(audio_path).info.length)
                        rerun()
                with wrong:
                    if button("❌", key="wrong_button", use_container_width=True, type="primary" if any(result[0] == flashcard['English'] and not result[2] for result in session_state.Results) else "secondary") and not session_state.show_wrongs:
                        session_state.Results = [result for result in session_state.Results if result[1] != flashcard['English']]
                        session_state.Results.append([int(current_index)+1, flashcard['English'], flashcard['Deutsch'], False])
                        session_state.flashcard_index = (current_index + 1) % total_flashcards
                        save_results()
                        audio_path = Path(f"cached_audios/{flashcard['Deutsch']}.mp3")
                        if not audio_path.exists():
                            audio_path = generate_audio(flashcard["Deutsch"])
                        with open(audio_path, "rb") as audio_file:
                            audio(audio_file, format="audio/mp3", autoplay=True)
                        sleep(MP3(audio_path).info.length)
                        rerun()
                with show_button:
                    with expander("Answer :", expanded=session_state.Show_all_anwsers):
                        markdown(f"{flashcard['Deutsch']}")
                        try:
                            audio_path = Path(f"cached_audios/{flashcard['Deutsch']}.mp3")
                            if not audio_path.exists():
                                audio_path = generate_audio(flashcard["Deutsch"])
                            with open(audio_path, "rb") as audio_file:
                                audio(audio_file, format="audio/mp3", autoplay=session_state.Show_all_anwsers)
                        except Exception as e:
                            write(f"Error generating audio: {str(e)}")
                        if session_state.auto_continue and session_state.Show_all_anwsers:
                            delay = slider(
                                "Switching Speed", 
                                min_value=0.25, 
                                max_value=3.0, 
                                value=1.0, 
                                step=0.25
                            )
                            sleep(MP3(audio_path).info.length + 2/delay)
                            session_state.flashcard_index = (current_index + 1) % total_flashcards
                            rerun()
                if not session_state.Show_all_anwsers:
                    check_answer(flashcard, current_index, total_flashcards)
            if not session_state.Show_all_anwsers and not session_state.show_wrongs:
                with expander(
                    f"👍🏼 Correct ({sum(r[3] == True for r in session_state.Results) / (l := len(session_state.Results) or 1) * 100:.1f}%)"
                    f" - 👎🏼 Wrong ({((wval := sum(r[3] == False for r in session_state.Results)) / l * 100):.1f}% - {wval})", expanded=True):
                    subheader("Wrong Answers")
                    dataframe([{'English : deutsch': f"{r[0]} - {r[1]} : {r[2]}"} for r in session_state.Results if r[3] == False][::-1], hide_index=True, use_container_width=True)
                    with popover(f"Unanswered ({100 - len(session_state.Results) / total_flashcards * 100:.1f}%)", icon="👉🏼"):
                        write(" | ".join([str(i + 1) for i, flashcard in flashcards_df.iterrows() if not any(result[1] == flashcard['English'] for result in session_state.Results)]))
        else:
            _, message_col, _ = columns([1, 2, 1], gap="small")
            with message_col:
                markdown("### ⚠️ No flashcards available. Please upload a valid file.")