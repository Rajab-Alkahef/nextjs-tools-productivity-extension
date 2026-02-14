"""
Main entry point for snippet viewer application
"""
import tkinter as tk
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extractors import SnippetExtractor
from gui import SnippetViewerGUI


def main():
    """Main function to run the snippet viewer GUI"""
    extractor = SnippetExtractor()
    extractor.extract_all_snippets()

    root = tk.Tk()
    app = SnippetViewerGUI(root, extractor)
    root.mainloop()


if __name__ == "__main__":
    main()
