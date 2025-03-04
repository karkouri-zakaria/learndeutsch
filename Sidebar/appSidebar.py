from pathlib import Path
from webbrowser import open as openURL
from Audio_gen.generate_audio import generate_audio
from streamlit import audio, expander,link_button, sidebar, text_area, write
class AppSidebar:
    def __init__(self):
        """Initialize the Sidebar class."""
        self.user_input = None
        self.front_text = None
        self.back_text = None
    def get_user_input(self):
        """Get user input for either text area or Verbformen search based on the toggle."""
        with sidebar:
            with expander("📖 Wörterbuch", expanded=False):
                verbformen_input = text_area(
                    label="---", 
                    placeholder="Word ...", 
                    key="verbformen_input",
                    height=68,
                    )
                link_button("Search",
                    help="Search for the word in the dictionary",
                    icon="🔍", use_container_width=True,
                    disabled=" " in verbformen_input or "" == verbformen_input,
                    url=f"https://www.verbformen.com/?w={verbformen_input.strip()}")
            with expander("🗣️ Text to Speech", expanded=False):
                self.user_input = text_area(
                    label="---",
                    placeholder="Text ...",
                    key="user_input",
                    height=68
                )
                if self.user_input.strip():
                    try:
                        audio_path = Path(f"cached_audios/{self.user_input.strip()}.mp3")
                        if not audio_path.exists():
                            audio_path = generate_audio(self.user_input.strip())
                        with open(audio_path, "rb") as audio_file:
                            audio(audio_file, format="audio/mp3", autoplay=True)
                    except Exception as e:
                        write(f"Error generating audio: {str(e)}")
