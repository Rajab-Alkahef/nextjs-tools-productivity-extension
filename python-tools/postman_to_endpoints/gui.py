"""
GUI application for Postman to TypeScript endpoints converter.
"""
import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
from postman_parser import walk_items
from code_generator import generate_ts_classes


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Postman → TypeScript EndPoints Converter")
        self.root.geometry("1100x700")

        # Dark theme colors
        self.bg_color = "#1e1e1e"
        self.fg_color = "#d4d4d4"
        self.button_bg = "#0e639c"
        self.button_hover = "#1177bb"
        self.entry_bg = "#252526"
        self.select_bg = "#37373d"
        self.text_bg = "#1e1e1e"
        self.text_fg = "#d4d4d4"
        self.status_bg = "#007acc"
        self.checkbox_bg = "#1e1e1e"
        self.checkbox_fg = "#d4d4d4"
        self.checkbox_select = "#007acc"

        # Configure root background
        self.root.configure(bg=self.bg_color)

        self._create_ui()
        self.current_path = None
        self.endpoints = []
        self.folder_vars = {}  # Dictionary to store folder checkbox variables

    def _create_ui(self):
        """Create the user interface components."""
        # Top frame with buttons
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.file_label = tk.Label(
            top_frame, text="No file selected", bg=self.bg_color, fg=self.fg_color, font=("Segoe UI", 9))
        self.file_label.pack(side=tk.LEFT, expand=True, anchor="w")

        browse_btn = tk.Button(
            top_frame, text="Browse Postman Collection", command=self.browse_file,
            bg=self.button_bg, fg="white", activebackground=self.button_hover,
            activeforeground="white", relief=tk.FLAT, padx=10, pady=5, font=("Segoe UI", 9))
        browse_btn.pack(side=tk.RIGHT, padx=5)

        generate_btn = tk.Button(
            top_frame, text="Generate", command=self.generate_code,
            bg=self.button_bg, fg="white", activebackground=self.button_hover,
            activeforeground="white", relief=tk.FLAT, padx=10, pady=5, font=("Segoe UI", 9))
        generate_btn.pack(side=tk.RIGHT, padx=5)

        copy_btn = tk.Button(
            top_frame, text="Copy to Clipboard", command=self.copy_to_clipboard,
            bg=self.button_bg, fg="white", activebackground=self.button_hover,
            activeforeground="white", relief=tk.FLAT, padx=10, pady=5, font=("Segoe UI", 9))
        copy_btn.pack(side=tk.RIGHT, padx=5)

        save_btn = tk.Button(
            top_frame, text="Save .ts File", command=self.save_file,
            bg=self.button_bg, fg="white", activebackground=self.button_hover,
            activeforeground="white", relief=tk.FLAT, padx=10, pady=5, font=("Segoe UI", 9))
        save_btn.pack(side=tk.RIGHT, padx=5)

        # Middle frame with folder selection and code preview
        middle_frame = tk.Frame(self.root, bg=self.bg_color)
        middle_frame.pack(side=tk.TOP, fill=tk.BOTH,
                          expand=True, padx=10, pady=(0, 10))

        # Left panel for folder selection
        left_panel = tk.Frame(middle_frame, bg=self.bg_color, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))

        folder_label = tk.Label(
            left_panel, text="Select Folders:", bg=self.bg_color, fg=self.fg_color,
            font=("Segoe UI", 10, "bold"), anchor="w")
        folder_label.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

        # Scrollable frame for checkboxes
        checkbox_frame = tk.Frame(left_panel, bg=self.bg_color)
        checkbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Canvas and scrollbar for folder selection
        canvas = tk.Canvas(checkbox_frame, bg=self.bg_color,
                           highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            checkbox_frame, orient="vertical", command=canvas.yview)
        self.checkbox_container = tk.Frame(canvas, bg=self.bg_color)

        self.checkbox_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window(
            (0, 0), window=self.checkbox_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Select all/none buttons
        select_buttons_frame = tk.Frame(left_panel, bg=self.bg_color)
        select_buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

        select_all_btn = tk.Button(
            select_buttons_frame, text="Select All", command=self.select_all_folders,
            bg=self.button_bg, fg="white", activebackground=self.button_hover,
            activeforeground="white", relief=tk.FLAT, padx=5, pady=3, font=("Segoe UI", 8))
        select_all_btn.pack(side=tk.LEFT, padx=2)

        select_none_btn = tk.Button(
            select_buttons_frame, text="Select None", command=self.select_none_folders,
            bg=self.button_bg, fg="white", activebackground=self.button_hover,
            activeforeground="white", relief=tk.FLAT, padx=5, pady=3, font=("Segoe UI", 8))
        select_none_btn.pack(side=tk.LEFT, padx=2)

        # Right panel for code preview
        right_panel = tk.Frame(middle_frame, bg=self.bg_color)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        code_label = tk.Label(
            right_panel, text="Generated Code:", bg=self.bg_color, fg=self.fg_color,
            font=("Segoe UI", 10, "bold"), anchor="w")
        code_label.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

        # Text area for generated code
        self.text_area = scrolledtext.ScrolledText(
            right_panel, wrap=tk.NONE, font=("Consolas", 10),
            bg=self.text_bg, fg=self.text_fg, insertbackground=self.fg_color,
            selectbackground=self.select_bg, selectforeground=self.fg_color,
            relief=tk.FLAT, borderwidth=1, highlightthickness=1,
            highlightbackground="#3e3e42", highlightcolor=self.button_bg)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar(
            value="Select a Postman collection JSON file to start.")
        status_bar = tk.Label(
            self.root, textvariable=self.status_var, anchor="w", relief=tk.SUNKEN, bd=1,
            bg=self.status_bg, fg="white", font=("Segoe UI", 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_file(self):
        """Browse and load a Postman collection JSON file."""
        file_path = filedialog.askopenfilename(
            title="Select Postman Collection JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return

        self.current_path = file_path
        self.file_label.config(text=os.path.basename(file_path))

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                collection = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read JSON file:\n{e}")
            self.status_var.set("Error reading file.")
            return

        items = collection.get("item", [])
        self.endpoints = list(walk_items(items))

        if not self.endpoints:
            messagebox.showwarning(
                "No endpoints", "No requests found in this collection.")
            self.status_var.set("No endpoints found.")
            return

        # Get unique folders
        folders = set()
        for _, _, _, folder in self.endpoints:
            folders.add(folder)

        # Clear existing checkboxes
        for widget in self.checkbox_container.winfo_children():
            widget.destroy()
        self.folder_vars = {}

        # Create checkboxes for each folder
        for folder in sorted(folders):
            var = tk.BooleanVar(value=True)  # Default to selected
            self.folder_vars[folder] = var

            checkbox = tk.Checkbutton(
                self.checkbox_container, text=folder, variable=var,
                bg=self.checkbox_bg, fg=self.checkbox_fg, selectcolor=self.checkbox_select,
                activebackground=self.checkbox_bg, activeforeground=self.checkbox_fg,
                font=("Segoe UI", 9), anchor="w", padx=5, pady=2)
            checkbox.pack(fill=tk.X, padx=5, pady=2)

        self.status_var.set(
            f"Loaded {len(self.endpoints)} endpoints from {len(folders)} folders. Select folders and click Generate.")

    def select_all_folders(self):
        """Select all folder checkboxes."""
        for var in self.folder_vars.values():
            var.set(True)

    def select_none_folders(self):
        """Deselect all folder checkboxes."""
        for var in self.folder_vars.values():
            var.set(False)

    def generate_code(self):
        """Generate TypeScript code for selected folders."""
        if not self.endpoints:
            messagebox.showwarning(
                "No endpoints", "Please load a Postman collection first.")
            return

        # Get selected folders
        selected_folders = {
            folder for folder, var in self.folder_vars.items() if var.get()
        }

        if not selected_folders:
            messagebox.showwarning(
                "No folders selected", "Please select at least one folder.")
            return

        ts_code = generate_ts_classes(self.endpoints, selected_folders)

        self.text_area.delete("1.0", tk.END)
        if ts_code:
            self.text_area.insert(
                tk.END, "// Generated from Postman collection\n\n")
            self.text_area.insert(tk.END, ts_code)
            count = sum(1 for _, _, _,
                        f in self.endpoints if f in selected_folders)
            self.status_var.set(
                f"Generated {count} endpoints from {len(selected_folders)} folder(s).")
        else:
            self.status_var.set("No endpoints to generate.")

    def save_file(self):
        """Save the generated TypeScript code to a file."""
        code = self.text_area.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning(
                "Nothing to save", "No code to save. Generate the class first.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save TypeScript File",
            defaultextension=".ts",
            filetypes=[("TypeScript files", "*.ts"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code + "\n")
            self.status_var.set(f"Saved to {file_path}")
            messagebox.showinfo("Saved", f"File saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")
            self.status_var.set("Error saving file.")

    def copy_to_clipboard(self):
        """Copy the generated TypeScript code to clipboard."""
        code = self.text_area.get("1.0", tk.END)
        if not code.strip():
            messagebox.showwarning(
                "Nothing to copy", "No code to copy. Generate the class first.")
            return

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(code)
            # keep clipboard after window closes
            self.root.update()
            self.status_var.set("Code copied to clipboard.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard:\n{e}")
            self.status_var.set("Error copying to clipboard.")
