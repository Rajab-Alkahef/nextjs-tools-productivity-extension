"""
GUI application for viewing code snippets
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SnippetViewerGUI:
    """GUI application for viewing code snippets"""

    def __init__(self, root, extractor):
        self.root = root
        self.extractor = extractor
        self.current_topic = None
        self.current_snippet_index = None

        # Dark mode color scheme
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.entry_bg = "#2d2d2d"
        self.entry_fg = "#ffffff"
        self.button_bg = "#0d7377"
        self.button_fg = "#ffffff"
        self.button_hover = "#14a085"
        self.frame_bg = "#252526"
        self.border_color = "#3c3c3c"
        self.select_bg = "#007acc"
        self.select_fg = "#ffffff"
        self.listbox_bg = "#2d2d2d"
        self.text_bg = "#1e1e1e"

        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.populate_topics()

    def setup_window(self):
        """Configure the main window"""
        self.root.title("Code Snippets Viewer - Generate Feature")
        self.root.geometry("1200x700")
        self.root.configure(bg=self.bg_color)
        self.root.minsize(800, 500)

    def setup_styles(self):
        """Configure ttk styles for dark mode"""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color,
                        foreground=self.fg_color)
        style.configure('TButton', background=self.button_bg,
                        foreground=self.button_fg)
        style.map('TButton', background=[('active', self.button_hover)])

    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            main_frame,
            text="Code Snippets from Generate Feature",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        title_label.pack(pady=(0, 10))

        # Content frame with three panels
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel - Topics
        left_panel = tk.Frame(content_frame, bg=self.frame_bg, relief='flat',
                              bd=1, highlightbackground=self.border_color, highlightthickness=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        left_panel.config(width=200)

        topics_label = tk.Label(
            left_panel,
            text="Topics",
            font=("Arial", 12, "bold"),
            bg=self.frame_bg,
            fg=self.fg_color
        )
        topics_label.pack(pady=10)

        # Topics listbox with scrollbar
        topics_frame = tk.Frame(left_panel, bg=self.frame_bg)
        topics_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))

        topics_scrollbar = tk.Scrollbar(topics_frame)
        topics_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.topics_listbox = tk.Listbox(
            topics_frame,
            bg=self.listbox_bg,
            fg=self.fg_color,
            selectbackground=self.select_bg,
            selectforeground=self.select_fg,
            font=("Consolas", 10),
            yscrollcommand=topics_scrollbar.set,
            relief='flat',
            borderwidth=0
        )
        self.topics_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.topics_listbox.bind('<<ListboxSelect>>', self.on_topic_select)
        topics_scrollbar.config(command=self.topics_listbox.yview)

        # Middle panel - Snippets
        middle_panel = tk.Frame(content_frame, bg=self.frame_bg, relief='flat',
                                bd=1, highlightbackground=self.border_color, highlightthickness=1)
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        middle_panel.config(width=250)

        snippets_label = tk.Label(
            middle_panel,
            text="Snippets",
            font=("Arial", 12, "bold"),
            bg=self.frame_bg,
            fg=self.fg_color
        )
        snippets_label.pack(pady=10)

        # Snippets listbox with scrollbar
        snippets_frame = tk.Frame(middle_panel, bg=self.frame_bg)
        snippets_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))

        snippets_scrollbar = tk.Scrollbar(snippets_frame)
        snippets_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.snippets_listbox = tk.Listbox(
            snippets_frame,
            bg=self.listbox_bg,
            fg=self.fg_color,
            selectbackground=self.select_bg,
            selectforeground=self.select_fg,
            font=("Consolas", 10),
            yscrollcommand=snippets_scrollbar.set,
            relief='flat',
            borderwidth=0
        )
        self.snippets_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.snippets_listbox.bind('<<ListboxSelect>>', self.on_snippet_select)
        snippets_scrollbar.config(command=self.snippets_listbox.yview)

        # Right panel - Code display
        right_panel = tk.Frame(content_frame, bg=self.frame_bg, relief='flat',
                               bd=1, highlightbackground=self.border_color, highlightthickness=1)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Code panel header
        code_header = tk.Frame(right_panel, bg=self.frame_bg)
        code_header.pack(fill=tk.X, padx=10, pady=10)

        code_label = tk.Label(
            code_header,
            text="Code Snippet",
            font=("Arial", 12, "bold"),
            bg=self.frame_bg,
            fg=self.fg_color
        )
        code_label.pack(side=tk.LEFT)

        # Copy buttons frame
        copy_buttons_frame = tk.Frame(code_header, bg=self.frame_bg)
        copy_buttons_frame.pack(side=tk.RIGHT)

        # Copy All button (hidden by default, shown for "All" topic)
        self.copy_all_btn = ttk.Button(
            copy_buttons_frame,
            text="Copy All Snippets",
            command=self.copy_all_snippets
        )
        self.copy_all_btn.pack(side=tk.LEFT, padx=(0, 5))
        self.copy_all_btn.pack_forget()  # Hide by default

        # Copy button
        self.copy_btn = ttk.Button(
            copy_buttons_frame,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard
        )
        self.copy_btn.pack(side=tk.LEFT)

        # Description label
        self.description_label = tk.Label(
            right_panel,
            text="Select a topic and snippet to view code",
            font=("Arial", 10),
            bg=self.frame_bg,
            fg=self.fg_color,
            wraplength=600,
            justify=tk.LEFT
        )
        self.description_label.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Code display area
        code_frame = tk.Frame(right_panel, bg=self.frame_bg)
        code_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.code_text = scrolledtext.ScrolledText(
            code_frame,
            bg=self.text_bg,
            fg=self.fg_color,
            font=("Consolas", 11),
            wrap=tk.WORD,
            relief='flat',
            borderwidth=0,
            padx=10,
            pady=10,
            insertbackground=self.fg_color
        )
        self.code_text.pack(fill=tk.BOTH, expand=True)
        self.code_text.config(state=tk.DISABLED)

        # Status bar
        status_frame = tk.Frame(main_frame, bg=self.frame_bg, relief='flat',
                                bd=1, highlightbackground=self.border_color, highlightthickness=1)
        status_frame.pack(fill=tk.X, pady=(10, 0))

        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=("Arial", 9),
            bg=self.frame_bg,
            fg=self.fg_color,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)

    def populate_topics(self):
        """Populate the topics listbox"""
        self.topics_listbox.delete(0, tk.END)
        for topic, snippet_list in self.extractor.snippets.items():
            if snippet_list:
                count = len(snippet_list)
                self.topics_listbox.insert(tk.END, f"{topic} ({count})")

        # Update status
        total_topics = len(
            [t for t, s in self.extractor.snippets.items() if s])
        total_snippets = sum(len(s) for s in self.extractor.snippets.values())
        self.status_label.config(
            text=f"Total: {total_topics} topics, {total_snippets} snippets")

    def on_topic_select(self, event):
        """Handle topic selection"""
        selection = self.topics_listbox.curselection()
        if not selection:
            return

        topic_index = selection[0]
        topic_name = self.topics_listbox.get(topic_index).split(" (")[0]
        self.current_topic = topic_name

        # Populate snippets for this topic
        self.snippets_listbox.delete(0, tk.END)
        if topic_name in self.extractor.snippets:
            for snippet in self.extractor.snippets[topic_name]:
                self.snippets_listbox.insert(tk.END, snippet['name'])

        # Show/hide Copy All button based on topic
        if topic_name == "All":
            self.copy_all_btn.pack(side=tk.LEFT, padx=(0, 5))
            self.copy_btn.pack(side=tk.LEFT)
            # Display all snippets combined
            self.display_all_snippets()
        else:
            self.copy_all_btn.pack_forget()
            # Clear code display
            self.code_text.config(state=tk.NORMAL)
            self.code_text.delete(1.0, tk.END)
            self.code_text.config(state=tk.DISABLED)
            self.description_label.config(text="Select a snippet to view code")

    def on_snippet_select(self, event):
        """Handle snippet selection"""
        if not self.current_topic:
            return

        selection = self.snippets_listbox.curselection()
        if not selection:
            return

        snippet_index = selection[0]
        self.current_snippet_index = snippet_index

        # Get the selected snippet
        snippet = self.extractor.snippets[self.current_topic][snippet_index]

        # Update description
        self.description_label.config(
            text=f"Description: {snippet['description']}")

        # Update code display
        self.code_text.config(state=tk.NORMAL)
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(1.0, snippet['code'])
        self.code_text.config(state=tk.DISABLED)

        # Update status
        self.status_label.config(
            text=f"Topic: {self.current_topic} | Snippet: {snippet['name']}")

    def display_all_snippets(self):
        """Display all snippets combined in VS Code format"""
        # Collect all snippets from all topics (except "All" itself)
        all_snippets_dict = {}

        for topic, snippet_list in self.extractor.snippets.items():
            if topic != "All" and snippet_list:
                for snippet in snippet_list:
                    # Extract the original snippet data from the JSON code
                    try:
                        snippet_json = json.loads(snippet['code'])
                        # Merge into all_snippets_dict
                        all_snippets_dict.update(snippet_json)
                    except json.JSONDecodeError:
                        # If parsing fails, skip this snippet
                        continue

        # Format as complete VS Code snippets JSON
        formatted_json = json.dumps(
            all_snippets_dict, indent="\t", ensure_ascii=False)

        # Update display
        self.code_text.config(state=tk.NORMAL)
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(1.0, formatted_json)
        self.code_text.config(state=tk.DISABLED)

        total_count = len(all_snippets_dict)
        self.description_label.config(
            text=f"All {total_count} snippets combined in VS Code format. Click 'Copy All Snippets' to copy the complete JSON."
        )
        self.status_label.config(
            text=f"All Snippets: {total_count} snippets ready to copy"
        )

    def copy_all_snippets(self):
        """Copy all snippets as a single VS Code snippets JSON object"""
        if self.current_topic != "All":
            return

        # Get the content from the code display
        all_content = self.code_text.get(1.0, tk.END).strip()

        if not all_content:
            messagebox.showwarning("Warning", "No snippets to copy")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(all_content)
        messagebox.showinfo(
            "Success", "All snippets copied to clipboard! You can paste this directly into your VS Code snippets file.")

    def copy_to_clipboard(self):
        """Copy current code snippet to clipboard"""
        if not self.current_topic:
            messagebox.showwarning("Warning", "Please select a topic first")
            return

        if self.current_topic == "All":
            # For "All" topic, copy the combined JSON
            self.copy_all_snippets()
            return

        if self.current_snippet_index is None:
            messagebox.showwarning("Warning", "Please select a snippet first")
            return

        snippet = self.extractor.snippets[self.current_topic][self.current_snippet_index]
        self.root.clipboard_clear()
        self.root.clipboard_append(snippet['code'])
        messagebox.showinfo("Success", "Code copied to clipboard!")
