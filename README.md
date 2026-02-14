# Next.js Productivity Tools - VS Code Extension

![Extension Icon](media/icon.png)

A VS Code extension that provides powerful productivity tools for Next.js development:
- **Feature Generator**: Generate complete Next.js feature structures with a GUI
- **Translation Extractor**: Extract, find missing, and manage translation keys
- **Postman to Endpoints Converter**: Convert Postman collections to TypeScript endpoint classes
- **Snippet Viewer**: Browse and copy VS Code snippets from generate feature templates

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

### 🔗 Postman to Endpoints Converter
- Convert Postman collection JSON files to TypeScript endpoint classes
- Select specific folders from your Postman collection to convert
- Generate TypeScript abstract classes with static endpoint properties
- Preview generated code before saving
- Copy to clipboard or save directly to `.ts` files
- Automatically handles Postman variables and URL formatting

### 📝 Snippet Viewer
- Browse code snippets extracted from generate feature templates
- View snippets organized by topic (Page Generation, Components, Hooks, Config, Types, Services, Redux, Routes, TypeScript)
- All snippets in VS Code snippet format (JSON with prefix, body, description)
- Copy individual snippets or all snippets at once
- "All" group combines all snippets into a single JSON object ready for VS Code snippets file
- Easy to add new snippets - just add them to the configuration files

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

### Postman to Endpoints Converter

1. Open Command Palette (Ctrl+Shift+P)
2. Type "Next.js Tools: Open Postman to Endpoints Converter"
3. Click "Browse Postman Collection" and select your Postman collection JSON file
4. Select the folders you want to convert (checkboxes on the left)
5. Click "Generate" to preview the TypeScript code
6. Review the generated code in the preview panel
7. Use "Copy to Clipboard" to copy the code, or "Save .ts File" to save it directly
8. The generated code will contain TypeScript abstract classes with static endpoint properties organized by folder

### Snippet Viewer

1. Open Command Palette (Ctrl+Shift+P)
2. Type "Next.js Tools: Open Snippet Viewer"
3. Browse snippets by topic in the left panel
4. Select a snippet to view its VS Code JSON format
5. Click "Copy to Clipboard" to copy individual snippets
6. Select "All" topic to see all snippets combined
7. Click "Copy All Snippets" to copy the complete JSON object
8. Paste the JSON directly into your VS Code snippets configuration file

**Snippet Topics Available:**
- **Page Generation**: Next.js page templates
- **Components**: React component templates
- **Hooks**: Custom React hooks
- **Config**: Form configuration with Zod validation
- **Types**: TypeScript interfaces
- **Services**: API endpoints, React Query hooks, mutations
- **Redux**: Redux slices and state management
- **Routes**: Route constants
- **TypeScript Snippets**: Common TypeScript patterns (13 snippets)
- **All**: Combined view of all snippets

**Adding New Snippets:**
- TypeScript snippets: Edit `web_scripts/snippet_viewer/snippets/typescript_snippets.py`
- Feature snippets: Edit the corresponding extractor file in `web_scripts/snippet_viewer/extractors/`

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
