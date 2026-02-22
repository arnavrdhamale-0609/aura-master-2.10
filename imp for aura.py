import subprocess
import sys

def install_packages(packages):
    """
    Install a list of Python packages using pip.
    """
    for package in packages:
        try:
            print(f"Installing: {package} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed: {package}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")
        except Exception as e:
            print(f"Unexpected error while installing {package}: {e}")

if __name__ == "__main__":
    packages_to_install = [
        "streamlit",
        "streamlit-webrtc",
        "mediapipe",
        "opencv-python-headless",
        "numpy",
        "av"
    ]

    print("Starting installation of required packages...")
    install_packages(packages_to_install)
    print("Installation process completed.")

