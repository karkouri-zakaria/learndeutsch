from hashlib import md5
from os import makedirs, path
from gtts import gTTS
from streamlit import cache_data

# Function to generate audio for the provided text
@cache_data
def generate_audio(text, lang="de", cache_dir="Audio_cache"):
    # Ensure the Audio_cache directory exists
    try:
        if not path.exists(cache_dir):
            makedirs(cache_dir)
    except OSError as e:
        raise OSError(f"Failed to create Audio_cache directory: {cache_dir}. Please check permissions.") from e

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
