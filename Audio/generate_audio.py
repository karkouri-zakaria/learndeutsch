from hashlib import md5
from os import makedirs, path
from gtts import gTTS
from streamlit import cache_data, session_state

# Function to generate audio for the provided text
@cache_data
def generate_audio(text, lang="de", cache_dir="Audio_cache"):
    # Ensure the Audio_cache directory exists
    makedirs(cache_dir, exist_ok=True)

    # Create a unique hash for the text to avoid re-generation
    audio_file = path.join(cache_dir, f"audio_{md5(text.encode()).hexdigest()}.mp3")

    # Check if the file already exists in the cache
    if not path.exists(audio_file):
        try:
            tts = gTTS(text=text, lang=lang) # German language
            tts.save(audio_file)
        except Exception as e:
            raise RuntimeError(f"Error generating audio: {e}") from e

    return audio_file

@cache_data
def generate_audio_files(flashcards_df, cache_dir="Audio_cache"):
    """Generate audio files for all flashcards."""
    if not session_state.get("audio_generated", False):
        makedirs(cache_dir, exist_ok=True)

        for _, flashcard in flashcards_df.iterrows():
            flashcard["audio_path"] = generate_audio(flashcard["BackText"], cache_dir=cache_dir)

        session_state.audio_generated = True