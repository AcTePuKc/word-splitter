
# Text/Word Splitter

A simple Python GUI application built with `tkinter` for splitting text files by lines, words, or characters. The app supports multiple languages (English, Spanish, Bulgarian, Russian and Chinese) and allows users to load files, split them, and save the results.

## Features

- Split text files by:
  - Lines
  - Words
  - Characters
- Split text files in half
- Choose from multiple file naming conventions for output files by holding Ctrl
- Supports multiple file formats including `.txt`, `.csv`, `.md`, `.json`, `.log`, `.xml`, `.yaml`, and more
- Multilingual support (English, Spanish, Bulgarian, Russian, Chinese (Simplified))
- Simple graphical interface (using `tkinter`)

## Requirements

- Python 3.x
- `tkinter` (typically pre-installed with Python on most systems)
- `json` (standard Python library)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/actepukc/text-word-splitter.git
   cd text-word-splitter
   ```



2. **Run the app:**
   Simply run the `word-splitter.py` file:
   ```bash
   python word-splitter.py
   ```

## How to Use

1. Open the application.
2. Load the text file(s) you want to split by clicking the **"Load File(s)"** button.
3. Select how you want to split the file (by lines, words, or characters) from the dropdown.
4. If needed, choose the number of lines, words, or characters to split the file by.
5. Click **"Split Text"** to generate the output files.
6. You can also split the file in half by clicking the **"Split in Half"** button.
7. Use the **Preferences** tab to change the output naming convention and language.

### Language Support

The app supports the following languages:
- English
- Spanish
- Bulgarian
- Russian
- Chinese (Simplified)

To change the language:
1. Go to the **Preferences** tab.
2. Select your desired language from the dropdown menu.
3. The app will update the UI text accordingly.

## Configuration

A `config.json` file is used to store the app's settings. The following settings are saved:
- **file_naming_method**: How the output files will be named (e.g., Original Filename + Number, Date-Time + Number, or Custom Format).
- **language**: The language used in the app's interface.
- **split_method**: The method used to split text files (by lines, words, or characters).

## Folder Structure
```bash
.
├── lang/                    # Directory containing language JSON files
│   ├── bg.json              # Bulgarian language translations
│   ├── eng.json             # English language translations
│   ├── es.json              # Spanish language translations
│   ├── ru.json              # Russian language translations
│   ├── zh-cn.json           # Simplified Chinese (Mainland China) translations
├── word-splitter.py         # Main application script that handles the GUI and functionality
├── README.md                # Project documentation (instructions for setup, usage, etc.)
└── requirements.txt         # List of Python dependencies required to run the application (if applicable)
```

## Known Issues

- When selecting an option from a dropdown, the internal key is sometimes shown instead of the translated text. This can be fixed by adjusting the translation logic within the app.

## To Do

- Improve error handling for unsupported file formats.
- Add support for additional languages.
- Package the application for macOS and Windows using `PyInstaller` or `auto-py-to-exe`.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
=======
# word-splitter
App to split almost any document/text to either lines/characters/words or half-words
