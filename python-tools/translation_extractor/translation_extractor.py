
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import json
import sys
import os

# Add current directory to path BEFORE importing local modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Now import local modules after path is set up
from generators.translation_generator import TranslationFileGenerator
from extractors.unused_keys_finder import UnusedKeysFinder
from extractors.missing_keys_finder import MissingKeysFinder
from extractors.translation_extractor import TranslationKeyExtractor
from extractors.hardcoded_extractor import HardcodedStringExtractor
import tkinter as tk


def scan_and_analyze():
    """Scan source directory and analyze translations"""
    source_dir = source_path.get().strip()
    translation_dir = translation_path.get().strip()

    if not source_dir:
        messagebox.showerror("Error", "Please select a source directory")
        return

    if not translation_dir:
        messagebox.showerror("Error", "Please select a translation directory")
        return

    source_path_obj = Path(source_dir)
    translation_path_obj = Path(translation_dir)

    if not source_path_obj.exists():
        messagebox.showerror("Error", "Source directory does not exist")
        return

    if not translation_path_obj.exists():
        messagebox.showerror("Error", "Translation directory does not exist")
        return

    # Disable buttons during processing
    scan_btn.config(state='disabled')
    update_btn.config(state='disabled')
    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, "Scanning... Please wait...\n")
    root.update()

    def process():
        try:
            results = {}

            # Extract translation keys
            if extract_keys.get():
                results_text.insert(tk.END, "Extracting translation keys...\n")
                root.update()
                extractor = TranslationKeyExtractor()
                extraction_results = extractor.extract_from_directory(
                    source_path_obj)
                results['extraction'] = extraction_results
                results_text.insert(
                    tk.END, f"Found {len(extraction_results['all_keys'])} translation keys\n")
                root.update()

            # Find hardcoded strings
            if find_hardcoded.get():
                results_text.insert(tk.END, "Finding hardcoded strings...\n")
                root.update()
                hardcoded_extractor = HardcodedStringExtractor()
                hardcoded_results = hardcoded_extractor.extract_from_directory(
                    source_path_obj)
                total_strings = sum(len(strings)
                                    for strings in hardcoded_results.values())
                results['hardcoded'] = hardcoded_results
                results_text.insert(
                    tk.END, f"Found {total_strings} hardcoded strings in {len(hardcoded_results)} files\n")
                if hardcoded_results:
                    results_text.insert(
                        tk.END, "\nFiles with hardcoded strings:\n")
                    for file_path, strings in hardcoded_results.items():
                        results_text.insert(
                            tk.END, f"  - {file_path} ({len(strings)} strings)\n")
                    results_text.insert(tk.END, "\nHardcoded strings found:\n")
                    for file_path, strings in hardcoded_results.items():
                        results_text.insert(tk.END, f"\n  File: {file_path}\n")
                        # Show first 10 per file
                        for string_info in strings[:10]:
                            text = string_info.get('text', '')
                            line = string_info.get('line', '?')
                            col = string_info.get('column', '?')
                            str_type = string_info.get('type', 'unknown')
                            suggested = string_info.get('suggested_key', '')
                            # Truncate long strings
                            display_text = text[:50] + \
                                "..." if len(text) > 50 else text
                            results_text.insert(
                                tk.END, f"    Line {line}:{col} [{str_type}] \"{display_text}\"")
                            if suggested:
                                results_text.insert(
                                    tk.END, f" → key: {suggested}")
                            results_text.insert(tk.END, "\n")
                        if len(strings) > 10:
                            results_text.insert(
                                tk.END, f"    ... and {len(strings) - 10} more strings in this file\n")
                root.update()

            # Find missing keys
            if find_missing.get():
                results_text.insert(
                    tk.END, f"Finding missing keys for locale '{locale_var.get()}'...\n")
                root.update()
                if 'extraction' in results:
                    finder = MissingKeysFinder(
                        translation_path_obj, locale_var.get())
                    missing_results = finder.find_missing_keys(
                        results['extraction']['all_keys'])
                    results['missing'] = missing_results
                    results_text.insert(
                        tk.END, f"Found {missing_results['missing_count']} missing keys\n")
                    results_text.insert(
                        tk.END, f"Total extracted keys: {missing_results['total_extracted']}\n")
                    results_text.insert(
                        tk.END, f"Existing keys in file: {missing_results['existing_count']}\n")
                    if missing_results['missing_keys']:
                        results_text.insert(tk.END, "\nMissing keys:\n")
                        for key in sorted(missing_results['missing_keys'])[:20]:
                            results_text.insert(tk.END, f"  - {key}\n")
                        if len(missing_results['missing_keys']) > 20:
                            results_text.insert(
                                tk.END, f"  ... and {len(missing_results['missing_keys']) - 20} more\n")
                    else:
                        results_text.insert(
                            tk.END, "\n✓ All keys found in translation file!\n")
                    root.update()
                else:
                    results_text.insert(
                        tk.END, "Error: Extract keys first to find missing keys\n")

            # Find unused keys
            if find_unused.get():
                results_text.insert(
                    tk.END, f"Finding unused keys for locale '{locale_var.get()}'...\n")
                root.update()
                if 'extraction' in results:
                    finder = UnusedKeysFinder(
                        translation_path_obj, locale_var.get())
                    unused_results = finder.find_unused_keys(
                        results['extraction']['all_keys'])
                    results['unused'] = unused_results
                    results_text.insert(
                        tk.END, f"Found {unused_results['unused_count']} unused keys\n")
                    if unused_results['unused_keys']:
                        results_text.insert(tk.END, "\nUnused keys:\n")
                        for detail in unused_results['unused_details'][:20]:
                            results_text.insert(
                                tk.END, f"  - {detail['key']}\n")
                        if len(unused_results['unused_keys']) > 20:
                            results_text.insert(
                                tk.END, f"  ... and {len(unused_results['unused_keys']) - 20} more\n")
                    root.update()
                else:
                    results_text.insert(
                        tk.END, "Error: Extract keys first to find unused keys\n")

            # Store results for update button
            global scan_results
            scan_results = results

            results_text.insert(tk.END, "\n✓ Scan completed!\n")
            messagebox.showinfo("Success", "Scan completed successfully!")

        except Exception as e:
            results_text.insert(tk.END, f"\n✗ Error: {str(e)}\n")
            messagebox.showerror("Error", f"Failed to scan: {str(e)}")
        finally:
            scan_btn.config(state='normal')
            update_btn.config(state='normal')

    # Run in separate thread to avoid blocking UI
    thread = threading.Thread(target=process)
    thread.daemon = True
    thread.start()


def update_translations():
    """Update translation files with missing keys"""
    translation_dir = translation_path.get().strip()
    locale = locale_var.get()

    if not translation_dir:
        messagebox.showerror("Error", "Please select a translation directory")
        return

    if 'missing' not in scan_results:
        messagebox.showerror("Error", "Please scan first to find missing keys")
        return

    missing_keys = scan_results['missing']['missing_keys']
    if not missing_keys:
        messagebox.showinfo("Info", "No missing keys to update")
        return

    # Confirm update
    response = messagebox.askyesno(
        "Confirm Update",
        f"Update translation file for locale '{locale}' with {len(missing_keys)} missing keys?\n\n"
        f"Keys will be added with placeholder values."
    )

    if not response:
        return

    try:
        translation_path_obj = Path(translation_dir)
        generator = TranslationFileGenerator(translation_path_obj, locale)
        update_results = generator.update_file(
            missing_keys, auto_fill=auto_fill.get())

        if update_results['success']:
            messagebox.showinfo(
                "Success",
                f"Successfully updated {update_results['added_count']} keys in {locale}.json\n\n"
                f"Skipped {update_results['skipped_count']} keys (already exist)"
            )
        else:
            messagebox.showerror("Error", "Failed to update translation file")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update: {str(e)}")


def browse_source_directory():
    """Browse for source directory"""
    directory = filedialog.askdirectory(title="Select Source Directory")
    if directory:
        source_path.set(directory)


def browse_translation_directory():
    """Browse for translation directory"""
    directory = filedialog.askdirectory(title="Select Translation Directory")
    if directory:
        translation_path.set(directory)


# Initialize results storage
scan_results = {}


# Create main window
root = tk.Tk()
root.title("Translation Key Extractor")
root.geometry("800x700")
root.resizable(True, True)

# Dark mode color scheme
bg_color = "#1e1e1e"
fg_color = "#ffffff"
entry_bg = "#2d2d2d"
entry_fg = "#ffffff"
button_bg = "#0d7377"
button_fg = "#ffffff"
button_hover = "#14a085"
frame_bg = "#252526"
border_color = "#3c3c3c"
select_bg = "#007acc"
select_fg = "#ffffff"
text_bg = "#1e1e1e"
text_fg = "#ffffff"

# Configure root window
root.configure(bg=bg_color)

# Configure ttk styles for dark mode
style = ttk.Style()
style.theme_use('clam')

# Configure styles
style.configure('TFrame', background=bg_color)
style.configure('TLabel', background=bg_color, foreground=fg_color)
style.configure('TLabelFrame', background=frame_bg,
                foreground=fg_color, bordercolor=border_color, relief='flat')
style.configure('TLabelFrame.Label', background=frame_bg, foreground=fg_color)
style.map('TLabelFrame', background=[
          ('active', frame_bg), ('focus', frame_bg)])
style.configure('TEntry', fieldbackground=entry_bg, foreground=entry_fg,
                bordercolor=border_color, insertcolor=fg_color)
style.map('TEntry',
          fieldbackground=[('disabled', '#1a1a1a'), ('!disabled', entry_bg)],
          foreground=[('disabled', '#666666'), ('!disabled', entry_fg)])
style.configure('TButton', background=button_bg,
                foreground=button_fg, bordercolor=button_bg, focuscolor='none')
style.map('TButton', background=[
          ('active', button_hover), ('pressed', button_bg)])
style.configure('TCheckbutton', background=frame_bg,
                foreground=fg_color, focuscolor='none')
style.map('TCheckbutton', background=[
          ('selected', frame_bg)], foreground=[('selected', fg_color)])
style.configure('TCombobox', fieldbackground=entry_bg, foreground=entry_fg,
                bordercolor=border_color)

# Variables
source_path = tk.StringVar()
translation_path = tk.StringVar()
locale_var = tk.StringVar(value='en')
extract_keys = tk.BooleanVar(value=True)
find_hardcoded = tk.BooleanVar(value=False)
find_missing = tk.BooleanVar(value=True)
find_unused = tk.BooleanVar(value=True)
auto_fill = tk.BooleanVar(value=False)

# Main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Title
title_label = tk.Label(
    main_frame, text="Translation Key Extractor", font=("Arial", 16, "bold"),
    bg=bg_color, fg=fg_color)
title_label.pack(pady=(0, 20))

# Source directory
source_label = tk.Label(main_frame, text="Source Directory:", font=("Arial", 10),
                        bg=bg_color, fg=fg_color)
source_label.pack(anchor=tk.W, pady=(0, 5))
source_frame = ttk.Frame(main_frame)
source_frame.pack(fill=tk.X, pady=(0, 15))
source_entry = ttk.Entry(
    source_frame, textvariable=source_path, width=50, font=("Arial", 10))
source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
source_browse_btn = ttk.Button(
    source_frame, text="Browse", command=browse_source_directory)
source_browse_btn.pack(side=tk.LEFT)

# Translation directory
translation_label = tk.Label(main_frame, text="Translation Directory (e.g., messages/):", font=("Arial", 10),
                             bg=bg_color, fg=fg_color)
translation_label.pack(anchor=tk.W, pady=(0, 5))
translation_frame = ttk.Frame(main_frame)
translation_frame.pack(fill=tk.X, pady=(0, 15))
translation_entry = ttk.Entry(
    translation_frame, textvariable=translation_path, width=50, font=("Arial", 10))
translation_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
translation_browse_btn = ttk.Button(
    translation_frame, text="Browse", command=browse_translation_directory)
translation_browse_btn.pack(side=tk.LEFT)

# Locale selection
locale_label = tk.Label(main_frame, text="Locale:", font=("Arial", 10),
                        bg=bg_color, fg=fg_color)
locale_label.pack(anchor=tk.W, pady=(0, 5))
locale_combo = ttk.Combobox(main_frame, textvariable=locale_var, width=20, font=("Arial", 10),
                            values=['en', 'ar', 'fr', 'es', 'de', 'it', 'pt', 'ru', 'zh', 'ja'])
locale_combo.pack(anchor=tk.W, pady=(0, 15))

# Options frame
options_container = tk.Frame(main_frame, bg=bg_color)
options_container.pack(fill=tk.X, pady=(0, 15))

# Options label
options_label = tk.Label(options_container, text="Options",
                         bg=bg_color, fg=fg_color, font=("Arial", 9, "bold"))
options_label.pack(anchor=tk.W, padx=5, pady=(0, 5))

# Options frame with border
options_frame = tk.Frame(options_container, bg=frame_bg, relief='flat',
                         bd=1, highlightbackground=border_color, highlightthickness=1)
options_frame.pack(fill=tk.X, padx=0, pady=0)

# Inner frame for padding
options_inner = tk.Frame(options_frame, bg=frame_bg)
options_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

# Checkboxes
extract_keys_check = ttk.Checkbutton(
    options_inner, text="Extract translation keys from code", variable=extract_keys)
extract_keys_check.pack(anchor=tk.W, pady=5)

find_hardcoded_check = ttk.Checkbutton(
    options_inner, text="Find hardcoded strings", variable=find_hardcoded)
find_hardcoded_check.pack(anchor=tk.W, pady=5)

find_missing_check = ttk.Checkbutton(
    options_inner, text="Find missing translation keys", variable=find_missing)
find_missing_check.pack(anchor=tk.W, pady=5)

find_unused_check = ttk.Checkbutton(
    options_inner, text="Find unused translation keys", variable=find_unused)
find_unused_check.pack(anchor=tk.W, pady=5)

auto_fill_check = ttk.Checkbutton(
    options_inner, text="Auto-fill missing keys with default values", variable=auto_fill)
auto_fill_check.pack(anchor=tk.W, pady=5)

# Results area
results_label = tk.Label(main_frame, text="Results:", font=("Arial", 10, "bold"),
                         bg=bg_color, fg=fg_color)
results_label.pack(anchor=tk.W, pady=(10, 5))

results_text = scrolledtext.ScrolledText(
    main_frame, width=80, height=15, font=("Consolas", 9),
    bg=text_bg, fg=text_fg, insertbackground=fg_color,
    relief='flat', borderwidth=1, highlightthickness=1,
    highlightbackground=border_color, highlightcolor=border_color)
results_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
results_text.insert(
    1.0, "Ready to scan. Select directories and click 'Scan' to begin.\n")

# Buttons frame
buttons_frame = ttk.Frame(main_frame)
buttons_frame.pack(fill=tk.X, pady=(10, 0))

scan_btn = ttk.Button(buttons_frame, text="Scan", command=scan_and_analyze)
scan_btn.pack(side=tk.LEFT, padx=(0, 10))

update_btn = ttk.Button(
    buttons_frame, text="Update Translations", command=update_translations)
update_btn.pack(side=tk.LEFT)

# Run the application
root.mainloop()
