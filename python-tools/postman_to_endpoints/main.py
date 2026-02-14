"""
Main entry point for Postman to TypeScript EndPoints Converter.
"""
import tkinter as tk
from gui import App


def main():
    """Initialize and run the application."""
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
