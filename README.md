# Next.js Productivity Tools - VS Code Extension

![Extension Icon](media/icon.png)

A VS Code extension that provides powerful productivity tools for Next.js development:
- **Feature Generator**: Generate complete Next.js feature structures with a GUI
- **Translation Extractor**: Extract, find missing, and manage translation keys
- **Other Feature**: Coming Soon....

## Features

### 🔥 Feature Generator
- Generate complete Next.js feature folder structures
- Support for dynamic routes, Redux, configs, mutations, and more
- Other Features

### 🌐 Translation Key Extractor
- Extract translation keys from code
- Find hardcoded strings that need translation
- Detect missing translation keys
- Find unused translation keys
- Update translation files automatically

## Requirements

- **Python 3.8+** installed on your system (with tkinter support)
  - Download from: https://www.python.org/downloads/
  - Make sure to check "Add Python to PATH" during installation
  - tkinter is included by default in standard Python installations
- VS Code 1.85.0 or higher (It is also work for Cursor)
- Windows (for GUI support)

## Usage

### Feature Generator

1. Open Command Palette (Ctrl+Shift+P)
2. Type "Next.js Tools: Open Feature Generator"
3. Enter feature name (e.g., "user profile")
4. Select output directory
5. Configure options
6. Click "Generate Feature"

### Translation Extractor

1. Open Command Palette (Ctrl+Shift+P)
2. Type "Next.js Tools: Open Translation Extractor"
3. Select source directory (your code)
4. Select translation directory (e.g., `messages/`)
5. Choose locale
6. Select options (extract keys, find hardcoded, find missing, etc.)
7. Click "Scan"
8. Review results and update translation files

## Extension Settings

No additional settings required. The extension uses your system Python installation.

**Note**: If you have Python installed but it's not in your PATH, you can:
1. Reinstall Python and check "Add Python to PATH"
2. Or manually add Python to your system PATH environment variable

## License

MIT 

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

MHD Rajab Alkahef  
[Email](rajabalkahef3@gmail.com) · [Website](https://rajab-alkahef.github.io/rajab-portfolio/) · [GitHub](https://github.com/Rajab-Alkahef) · 
[GitLab](https://gitlab.com/Rajab-Alkahef) · [LinkedIn](https://www.linkedin.com/in/rajabalkahef/) · 
[Youtube](https://www.youtube.com/@rajabalkahef) · [Instagram](https://www.instagram.com/rajab.alkahef) · 
[Facebook](https://www.facebook.com/rajabalkahef)
