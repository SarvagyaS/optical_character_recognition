# Passport OCR Project

## Overview
This project implements an Optical Character Recognition (OCR) system specifically designed for recognizing and extracting information from passport images. The system utilizes the `pytesseract` library for text extraction and `OpenCV` for image processing.

## Folder Structure
The project is organized into the following directories and files:

```
passport_ocr/
├── config/               # Configuration files for model parameters and settings
│   └── settings.json
├── data/                 # Input passport image samples
├── images/               # Processed passport images
├── models/               # OCR models or pretrained models
├── src/                  # Source code for the project
│   ├── __init__.py       # Marks the src directory as a Python package
│   ├── ocr.py            # OCR processing logic
│   ├── utils.py          # Helper functions for image preprocessing
│   └── passport_recognition.py  # Main logic for passport text recognition
├── .gitignore            # Files and directories to ignore by Git
├── LICENSE               # Licensing information for the project
├── README.md             # Documentation for project setup and usage
└── requirements.txt      # List of necessary libraries
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd passport_ocr
   ```

2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

## Usage
To recognize text from a passport image, use the `passport_recognition.py` script. Here’s a basic example:

```python
from src.passport_recognition import recognize_passport

image_path = 'data/sample_passport.jpg'
passport_info = recognize_passport(image_path)
print(passport_info)
```

## Configuration
Adjust the settings in `config/settings.json` to modify model parameters and image processing settings as needed.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.