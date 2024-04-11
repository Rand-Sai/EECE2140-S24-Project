# EECE2140-S24-Project
This is the git repository for the final project of class EECE2140 for spring semester 2024.

## Introduction
This is a simple QR Code Application developed using Python. It allows users to generate QR codes from text or URLs, analyze QR codes from image files, and scan QR codes using a camera.

## Installation
1. Clone this repository to your local machine:
git clone https://github.com/Rand-Sai/EECE2140-S24-Project.git
2. Navigate to the project directory:
cd QR_Code_Application
3. Install the required dependencies:
pip install qrcode opencv-python-headless pillow PyQt5

## Usage
1. Run the application by executing the `main.py` file:
python main.py

2. The application window will open, presenting you with several options:
- **Generate QR Code**: Allows you to generate a QR code from text or a URL. You can specify the file name and color of the QR code.
- **Analyze QR Code**: Enables you to analyze a QR code from an image file and display the information stored in it.
- **Scan QR Code with Camera**: Opens your camera to scan a QR code. Once detected, it displays the information stored in the QR code.
- **Exit**: Closes the application.

## Requirements
- Python 3.x
- qrcode
- opencv-python-headless
- pillow

## Contributors
- Sai Him Yuan
- Zekun Lin

## License
This project is licensed under the MIT License.
