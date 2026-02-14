
from utils import to_camel_case, to_pascal_case
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import sys
import os

# Add current directory to path BEFORE importing local modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Now import local modules after path is set up
from generators import (
    page_generator,
    components_generator,
    hooks_generator,
    config_generator,
    types_generator,
    services_generator,
    redux_generator,
    routes_generator
)

def generate_feature():
    feature_name = feature_name_entry.get().strip()

    if not feature_name:
        messagebox.showerror("Error", "Please enter a feature name")
        return

    if not output_path.get():
        messagebox.showerror("Error", "Please select an output directory")
        return

    # Convert names
    camel_case_name = to_camel_case(feature_name)
    pascal_case_name = to_pascal_case(feature_name)

    # Get base path
    base_path = Path(output_path.get())
    feature_path = base_path / camel_case_name

    try:
        # Create main feature folder
        feature_path.mkdir(parents=True, exist_ok=True)

        # Generate page.tsx
        page_generator.generate_page(
            feature_path, feature_name, use_dynamic_route.get())

        # Generate components folder
        components_generator.generate_components(feature_path, feature_name)

        # Generate hooks folder
        hooks_generator.generate_hooks(feature_path, feature_name)

        # Generate config folder (optional)
        if include_config.get():
            config_file_name = config_name_entry.get().strip() or None
            config_generator.generate_config(
                feature_path, feature_name, config_file_name)

        # Generate types folder
        types_generator.generate_types(feature_path, feature_name)

        # Generate services folder (endpoints and queries)
        query_file_name = query_name_entry.get().strip() or None
        services_generator.generate_services(
            feature_path, feature_name, query_file_name)

        # Generate mutations folder (optional)
        if include_mutations.get():
            mutation_file_name = mutation_name_entry.get().strip()
            if not mutation_file_name:
                messagebox.showerror(
                    "Error", "Please enter a mutation file name")
                return
            services_generator.generate_mutations(
                feature_path, feature_name, mutation_file_name)

        # Generate redux folder (optional)
        if include_redux.get():
            redux_generator.generate_redux(feature_path, feature_name)

        # Generate routes folder (optional)
        if include_routes.get():
            routes_generator.generate_routes(feature_path, feature_name)

        messagebox.showinfo(
            "Success", f"Feature '{camel_case_name}' generated successfully at:\n{feature_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate feature: {str(e)}")


def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_path.set(directory)


def toggle_config():
    if include_config.get():
        config_name_entry.config(state='normal')
    else:
        config_name_entry.config(state='disabled')


def toggle_mutations():
    if include_mutations.get():
        mutation_name_entry.config(state='normal')
    else:
        mutation_name_entry.config(state='disabled')


# Create main window
root = tk.Tk()
root.title("Next.js Feature Generator")
root.geometry("600x700")
root.resizable(False, False)

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

# Variables
feature_name_entry = tk.StringVar()
output_path = tk.StringVar()
use_dynamic_route = tk.BooleanVar()
include_config = tk.BooleanVar()
include_mutations = tk.BooleanVar()
include_redux = tk.BooleanVar()
include_routes = tk.BooleanVar()

# Main frame
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Title
title_label = tk.Label(
    main_frame, text="Next.js Feature Generator", font=("Arial", 16, "bold"),
    bg=bg_color, fg=fg_color)
title_label.pack(pady=(0, 20))

# Feature name
feature_name_label = tk.Label(main_frame, text="Feature Name: (make space between words for example: test two)", font=("Arial", 10),
                              bg=bg_color, fg=fg_color)
feature_name_label.pack(anchor=tk.W, pady=(0, 5))
feature_entry = ttk.Entry(
    main_frame, textvariable=feature_name_entry, width=50, font=("Arial", 10))
feature_entry.pack(fill=tk.X, pady=(0, 15))

# Output directory
output_dir_label = tk.Label(main_frame, text="Output Directory:", font=("Arial", 10),
                            bg=bg_color, fg=fg_color)
output_dir_label.pack(anchor=tk.W, pady=(0, 5))
dir_frame = ttk.Frame(main_frame)
dir_frame.pack(fill=tk.X, pady=(0, 15))
output_dir_entry = ttk.Entry(
    dir_frame, textvariable=output_path, width=40, font=("Arial", 10))
output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
browse_btn = ttk.Button(dir_frame, text="Browse", command=browse_directory)
browse_btn.pack(side=tk.LEFT)

# Options frame - using tk.Frame for better dark mode support
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

# Dynamic route checkbox
dynamic_route_check = ttk.Checkbutton(
    options_inner, text="Put page.tsx inside [[...id]] folder", variable=use_dynamic_route)
dynamic_route_check.pack(anchor=tk.W, pady=5)

# Config checkbox
config_check = ttk.Checkbutton(
    options_inner, text="Include config folder", variable=include_config, command=toggle_config)
config_check.pack(anchor=tk.W, pady=5)

config_label = tk.Label(options_inner, text="Config file name (optional):",
                        font=("Arial", 9), bg=frame_bg, fg=fg_color)
config_label.pack(anchor=tk.W, pady=(5, 0))
config_name_entry = ttk.Entry(options_inner, width=40, font=("Arial", 9))
config_name_entry.pack(anchor=tk.W, fill=tk.X, pady=(0, 10))
config_name_entry.config(state='disabled')

# Mutations checkbox
mutations_check = ttk.Checkbutton(
    options_inner, text="Include mutations folder", variable=include_mutations, command=toggle_mutations)
mutations_check.pack(anchor=tk.W, pady=5)

mutation_label = tk.Label(options_inner, text="Mutation file name (required if checked):",
                          font=("Arial", 9), bg=frame_bg, fg=fg_color)
mutation_label.pack(anchor=tk.W, pady=(5, 0))
mutation_name_entry = ttk.Entry(options_inner, width=40, font=("Arial", 9))
mutation_name_entry.pack(anchor=tk.W, fill=tk.X, pady=(0, 10))
mutation_name_entry.config(state='disabled')

# Redux checkbox
redux_check = ttk.Checkbutton(
    options_inner, text="Include redux folder", variable=include_redux)
redux_check.pack(anchor=tk.W, pady=5)

# Routes checkbox
routes_check = ttk.Checkbutton(
    options_inner, text="Include routes folder", variable=include_routes)
routes_check.pack(anchor=tk.W, pady=5)

# Query name
query_label = tk.Label(options_inner, text="Query file name (optional, defaults to useGetAll{FeatureName}):",
                       font=("Arial", 9), bg=frame_bg, fg=fg_color)
query_label.pack(anchor=tk.W, pady=(5, 0))
query_name_entry = ttk.Entry(options_inner, width=40, font=("Arial", 9))
query_name_entry.pack(anchor=tk.W, fill=tk.X, pady=(0, 10))

# Generate button
generate_btn = ttk.Button(
    main_frame, text="Generate Feature", command=generate_feature)
generate_btn.pack(pady=20)

# Run the application
root.mainloop()
