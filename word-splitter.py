import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
import json
from datetime import datetime

# App Info
app_name = "Text/Word Splitter"
version = "1.0"

# Global variables
content = ""
output_dir = ""
file_base_name = ""
file_naming_method = "Original Filename + Number"
method_var = None
file_namin_var = None
settings = {}
language_data = {}


# Initialization phase
initial_load = True

# Load settings from config.json or use available language file if config.json is missing
def load_settings():
    global settings, initial_load
    try:
        with open('config.json', 'r', encoding='utf-8') as f:  # Ensure UTF-8 encoding
            settings = json.load(f)
    except FileNotFoundError:
        # Scan for available languages
        available_languages = scan_for_languages()
        if available_languages:
            # Default settings if config.json is not found
            settings = {"file_naming_method": "original_filename_number", "language": list(available_languages.keys())[0], "split_method": "lines"}
            save_settings()  # Save the default settings to a new config.json file
        else:
            messagebox.showerror("Error", "No language files found! Exiting.")
            root.destroy()
    
    # Apply settings to the UI
    file_naming_var.set(settings.get("file_naming_method", "original_filename_number"))
    selected_language.set(settings.get("language", "eng"))
    method_var.set(settings.get("split_method", "lines"))

    update_settings()  # Apply loaded settings to the UI elements
    
    # End of initialization phase
    initial_load = False


# Save settings to config.json
def save_settings():
    settings["file_naming_method"] = file_naming_var.get()  # Save the internal key
    settings["language"] = selected_language.get()
    settings["split_method"] = method_var.get()  # Save the internal key
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False)

# Update the file naming dropdown
def update_file_naming_dropdown():
    file_naming_menu['menu'].delete(0, 'end')  # Clear existing options
    for option_key, option_value in language_data['naming_options'].items():
        file_naming_menu['menu'].add_command(label=option_value, 
                                             command=lambda value=option_value, key=option_key: update_file_naming(key, value))
    current_naming_key = next((k for k, v in language_data['naming_options'].items() if v == file_naming_var.get()), file_naming_var.get())
    update_file_naming(current_naming_key)

    # Set the current value to the translated version
    current_key = file_naming_var.get()
    file_naming_var.set(language_data['naming_options'].get(current_key, current_key))

# Update settings UI from loaded settings
def update_settings():
    file_naming_var.set(settings.get("file_naming_method", "Original Filename + Number"))
    selected_language.set(settings.get("language", "eng"))

# Scan the 'lang' folder for all available language files
def scan_for_languages():
    lang_dir = os.path.join(os.path.dirname(__file__), 'lang')
    available_languages = {}
    if os.path.exists(lang_dir):
        for filename in os.listdir(lang_dir):
            if filename.endswith('.json'):
                lang_code = filename.split('.')[0]
                available_languages[lang_code] = os.path.join(lang_dir, filename)
    return available_languages

# Load the selected language file
def load_language():
    global language_data
    lang_file_path = available_languages.get(selected_language.get(), "lang/eng.json")
    try:
        with open(lang_file_path, 'r', encoding='utf-8') as f:
            language_data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Language file {lang_file_path} not found.")
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"Error reading language file: {e}")

# Apply the loaded language to the UI
def apply_language():
    global method_var, file_naming_var
    
    root.title(f"{language_data.get('app_name', app_name)} v{language_data.get('version', version)}")
    
    # Update notebook tab names
    notebook.tab(main_tab, text=language_data.get("main_tab", "Main"))
    notebook.tab(preferences_tab, text=language_data.get("preferences_tab", "Preferences"))
    notebook.tab(how_to_use_tab, text=language_data.get("how_to_use_tab", "How to Use"))

    # Update UI elements in Main tab
    load_button.config(text=language_data.get("load_file", "Load File(s)"))
    method_label.config(text=language_data.get("split_by", "Split by:"))
    split_button.config(text=language_data.get("split_text", "Split Text"))
    split_in_half_button.config(text=language_data.get("split_in_half", "Split in Half"))
    split_amount_label.config(text=language_data.get("split_amount_label", "Split amount:"))
    save_button.config(text=language_data.get("save_settings", "Save Settings"))

    # Update method dropdown (Split by)
    current_method = method_var.get()
    method_menu['menu'].delete(0, 'end')
    for option_key, option_value in language_data['split_options'].items():
        method_menu['menu'].add_command(label=option_value, 
                                        command=lambda v=option_value, k=option_key: method_var.set(v))
    translated_method = language_data['split_options'].get(current_method, current_method)
    method_var.set(translated_method)

    # Update file naming dropdown (File Naming Convention)
    current_naming = file_naming_var.get()
    file_naming_menu['menu'].delete(0, 'end')
    for option_key, option_value in language_data['naming_options'].items():
        file_naming_menu['menu'].add_command(label=option_value, 
                                             command=lambda v=option_value, k=option_key: file_naming_var.set(v))
    translated_naming = language_data['naming_options'].get(current_naming, current_naming)
    file_naming_var.set(translated_naming)

    # Update Preferences tab
    naming_label.config(text=language_data.get("file_naming_convention", "File Naming Convention"))
    language_label.config(text=language_data.get("language", "Language"))
    
    # Update How to Use tab
    how_to_use_label.config(text=language_data.get("instructions", "Instructions will appear here."))

def update_method_dropdown():
    method_menu['menu'].delete(0, 'end')  # Clear existing options
    for option_key, option_value in language_data['split_options'].items():
        method_menu['menu'].add_command(label=option_value, 
                                        command=lambda value=option_value, key=option_key: update_method(key, value))
    current_method_key = next((k for k, v in language_data['split_options'].items() if v == method_var.get()), method_var.get())
    update_method(current_method_key)

# Set the current value to the translated version
def update_method(key, value=None):
    method_var.set(language_data['split_options'].get(key, key))

# Set the current value to the translated version
def update_file_naming(key, value=None):
    file_naming_var.set(language_data['naming_options'].get(key, key))

# Function to load file and show stats
def load_file():
    global content, file_base_name
    try:
        file_paths = filedialog.askopenfilenames(
            title=language_data.get("load_file", "Load File(s)"),
            filetypes=[("Text Files", "*.txt"), ("Markdown Files", "*.md"), ("CSV Files", "*.csv"),
                       ("JSON Files", "*.json"), ("Log Files", "*.log"), ("XML Files", "*.xml"),
                       ("YAML Files", "*.yaml"), ("All Files", "*.*")]
        )
        
        if not file_paths:
            return

        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            file_base_name = os.path.basename(file_path).split('.')[0]

            num_lines = len(content.splitlines())
            num_words = len(content.split())
            num_chars = len(content)

            log(f"{language_data.get('loaded_file', 'Loaded file')}: {file_base_name}.txt")
            log(f"{language_data.get('lines', 'Lines')}: {num_lines}, {language_data.get('words', 'Words')}: {num_words}, {language_data.get('characters', 'Characters')}: {num_chars}")

            loaded_file_label.config(text=f"{language_data.get('loaded_file', 'Loaded file')}: {file_base_name}.txt")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to log messages to the console
def log(message):
    console_text.config(state=tk.NORMAL)
    console_text.insert(tk.END, message + "\n")
    console_text.config(state=tk.DISABLED)
    console_text.yview(tk.END)

# Function to split the text in half by words and save the two parts
def split_in_half():
    global content, file_base_name, output_dir
    try:
        split_in_half_button.config(state=tk.DISABLED)
        root.update()

        words = content.split()
        half_index = len(words) // 2

        first_half = ' '.join(words[:half_index])
        second_half = ' '.join(words[half_index:])

        log(language_data.get("splitting_in_half", "Splitting the file in half..."))
        log(f"{language_data.get('first_half_length', 'First half length')}: {len(first_half.split())} {language_data.get('words', 'words')}")
        log(f"{language_data.get('second_half_length', 'Second half length')}: {len(second_half.split())} {language_data.get('words', 'words')}")

        root.after(500)

        if not output_dir:
            output_dir = filedialog.askdirectory(title=language_data.get("select_output_dir", "Select Output Directory"))
            if not output_dir:
                return

        first_half_file = os.path.join(output_dir, f"{file_base_name}_part1.txt")
        second_half_file = os.path.join(output_dir, f"{file_base_name}_part2.txt")

        with open(first_half_file, 'w', encoding='utf-8') as f1, open(second_half_file, 'w', encoding='utf-8') as f2:
            f1.write(first_half)
            f2.write(second_half)

        log(language_data.get("file_saved", "File saved as") + f" {first_half_file}")
        log(language_data.get("file_saved", "File saved as") + f" {second_half_file}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        split_in_half_button.config(state=tk.NORMAL)


# Function to split text
def split_text():
    global content, file_base_name, output_dir
    try:
        split_method = method_var.get()
        split_amount = int(split_amount_entry.get())

        if split_method == language_data['split_options'].get('lines', 'Lines'):
            chunks = ['\n'.join(content.splitlines()[i:i+split_amount]) for i in range(0, len(content.splitlines()), split_amount)]
        elif split_method == language_data['split_options'].get('words', 'Words'):
            words = content.split()
            chunks = [' '.join(words[i:i+split_amount]) for i in range(0, len(words), split_amount)]
        elif split_method == language_data['split_options'].get('characters', 'Characters'):
            chunks = [content[i:i+split_amount] for i in range(0, len(content), split_amount)]

        log(f"Splitting using {split_method}")
        log(f"Total chunks: {len(chunks)}")

        root.after(500)

        if not output_dir:
            output_dir = filedialog.askdirectory(title=language_data.get("select_output_dir", "Select Output Directory"))
            if not output_dir:
                return

        for i, chunk in enumerate(chunks):
            chunk_file = os.path.join(output_dir, f"{file_base_name}_chunk{i+1}.txt")
            with open(chunk_file, 'w', encoding='utf-8') as f:
                f.write(chunk)

            log(language_data.get("file_saved", "File saved as") + f" {chunk_file}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Use the selected key when saving settings
def on_settings_changed():
    global settings
    # Get the key corresponding to the selected translated value
    selected_value = file_naming_var.get()
    selected_key = next((k for k, v in language_data['naming_options'].items() if v == selected_value), selected_value)
    settings["file_naming_method"] = selected_key

    settings["file_naming_method"] = file_naming_var.get()  # Use the internal keys
    settings["language"] = selected_language.get()
    settings["split_method"] = method_var.get()  # Use the internal keys
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False)

    log(language_data.get("settings_saved", "Settings saved!"))
    
# Handle language change immediately after selection
def on_language_changed(*args):
    global initial_load
    if not initial_load:  # Only log after the initial load
        log(f"{language_data.get('language_changed', 'Language changed')}: {selected_language.get()}")
    load_language()
    apply_language()


# Create the main application window
root = tk.Tk()


# Check if icon.ico exists and set it as the icon
icon_path = "icon.ico"
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    print("icon.ico not found, using default icon")
    
# Create a notebook (tabs) widget
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Create frames for each tab
main_tab = ttk.Frame(notebook)
preferences_tab = ttk.Frame(notebook)
how_to_use_tab = ttk.Frame(notebook)

notebook.add(main_tab, text="Main")
notebook.add(preferences_tab, text="Preferences")
notebook.add(how_to_use_tab, text="How to Use")

# Main tab content
# app_label = tk.Label(main_tab, font=("Arial", 14, "bold"))
# app_label.pack(pady=10)

loaded_file_label = tk.Label(main_tab, text="", font=("Arial", 10))
loaded_file_label.pack(pady=5)

left_frame = tk.Frame(main_tab)
left_frame.pack(side=tk.LEFT, padx=10)

right_frame = tk.Frame(main_tab)
right_frame.pack(side=tk.RIGHT, padx=10)

# Left frame: Load button and method options
load_button = tk.Button(left_frame, text="Load File(s)", command=load_file)
load_button.pack(pady=10)

method_label = tk.Label(left_frame, text="Split by:")
method_label.pack(pady=5)

method_var = tk.StringVar(value="Lines")
method_options = ["Lines", "Words", "Characters"]
method_menu = tk.OptionMenu(left_frame, method_var, *method_options)
method_menu.pack(pady=5)

split_amount_label = tk.Label(left_frame, text="Split amount:")
split_amount_label.pack(pady=5)

split_amount_entry = tk.Entry(left_frame)
split_amount_entry.pack(pady=5)

# Right frame: Split buttons
split_button = tk.Button(right_frame, text="Split Text", command=split_text)
split_button.pack(pady=20)

split_in_half_button = tk.Button(right_frame, text="Split in Half", command=split_in_half)
split_in_half_button.pack(pady=20)

# Preferences tab content
naming_label = tk.Label(preferences_tab, text=language_data.get("file_naming_convention", "File Naming Convention:"))
naming_label.pack(pady=10)

file_naming_var = tk.StringVar(value="Original Filename + Number")


# Preferences tab content
naming_options = {
    "original_filename_number": language_data.get("original_filename_number", "Original Filename + Number"),
    "date_time_number": language_data.get("date_time_number", "Date-Time + Number"),
    "custom_format": language_data.get("custom_format", "Custom Format")
}
# Display translated options, but save internal keys
file_naming_menu = tk.OptionMenu(preferences_tab, file_naming_var, *naming_options.keys())
file_naming_menu.pack(pady=10)


# Language dropdown content
available_languages = scan_for_languages()
selected_language = tk.StringVar(value=settings.get("language", "eng"))
language_label = tk.Label(preferences_tab, text="Language:")
language_label.pack(pady=10)
language_menu = tk.OptionMenu(preferences_tab, selected_language, *available_languages.keys())
language_menu.pack(pady=10)

# Display translated options, but save internal keys
selected_language.trace_add('write', on_language_changed)

# Save button
save_button = tk.Button(preferences_tab, text="Save Settings", command=on_settings_changed)
save_button.pack(pady=10)

save_button.config(text=language_data.get("save_settings", "Save Settings"))

# Console output
console_text = scrolledtext.ScrolledText(main_tab, wrap=tk.WORD, height=10, state=tk.DISABLED)
console_text.pack(pady=10, fill=tk.BOTH, expand=True)

# How to Use Tab content
how_to_use_label = tk.Label(how_to_use_tab, wraplength=400)
how_to_use_label.pack(pady=20)

# Load settings and language on start
load_settings()
load_language()
apply_language()

root.mainloop()
