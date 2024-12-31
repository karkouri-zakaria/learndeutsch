
from os import system
from subprocess import CalledProcessError, check_call
from sys import executable


def ensure_streamlit_installed():
    try:
        check_call([executable, "-m", "pip", "show", "streamlit"])
    except CalledProcessError:
        print("Streamlit is not installed. Installing...")
        check_call([executable, "-m", "pip", "install", "streamlit"])

if __name__ == "__main__":
    ensure_streamlit_installed()
    app_file = "path/to/your_app.py"  # Replace with your app's path
    system(f"streamlit run {app_file}")