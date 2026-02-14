import { spawn } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';

/**
 * Spawns a Python tool with the embedded Python runtime
 */
function spawnPythonTool(
    context: vscode.ExtensionContext,
    scriptRelPath: string,
    args: string[] = []
): void {
    const extRoot = context.extensionPath;
    const scriptPath = path.join(extRoot, 'python-tools', scriptRelPath);

    // Try to find Python executable
    // First try embedded Python (if it exists), then fall back to system Python
    let pythonExe: string | null = null;

    // Check for embedded Python first (optional)
    const embeddedPython = path.join(extRoot, 'python-runtime', 'python.exe');
    if (fs.existsSync(embeddedPython)) {
        pythonExe = embeddedPython;
        console.log('Using embedded Python runtime');
    } else {
        // Use system Python (python.exe for GUI apps - no console window)
        pythonExe = 'python';
        console.log('Using system Python (python)');
    }

    // Check if script exists
    if (!fs.existsSync(scriptPath)) {
        vscode.window.showErrorMessage(
            `Python script not found at: ${scriptPath}`
        );
        return;
    }

    // If using system Python, verify it's available
    if (pythonExe === 'python') {
        // Try to verify Python is available by checking version
        const testProcess = spawn('python', ['--version'], { shell: true });
        testProcess.on('error', () => {
            vscode.window.showErrorMessage(
                `Python not found in system PATH.\n\n` +
                `Please install Python from https://www.python.org/downloads/\n` +
                `Make sure to check "Add Python to PATH" during installation.\n\n` +
                `Alternatively, you can use embedded Python by adding it to python-runtime/ folder.`
            );
        });
        testProcess.on('exit', (code) => {
            if (code !== 0) {
                vscode.window.showWarningMessage(
                    `Python may not be properly installed. The tool will still attempt to run.`
                );
            }
        });
    }

    // Get the script directory for working directory
    const scriptDir = path.dirname(scriptPath);

    // Spawn Python process with error capture
    // Use shell: true for system Python (python) to find it in PATH
    const useShell = pythonExe === 'python';
    const child = spawn(pythonExe, [scriptPath, ...args], {
        cwd: scriptDir,
        shell: useShell,
        stdio: ['ignore', 'pipe', 'pipe'] // Capture stdout and stderr to see errors
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => {
        const output = data.toString();
        stdout += output;
        console.log(`[PYTHON OUT]: ${output}`);
    });

    child.stderr.on('data', (data) => {
        const output = data.toString();
        stderr += output;
        console.error(`[PYTHON ERR]: ${output}`);
    });

    child.on('error', (err) => {
        const errorMsg = `Failed to start Python tool: ${err.message}\n\n` +
            `Python executable: ${pythonExe}\n` +
            `Script path: ${scriptPath}\n` +
            `Working directory: ${scriptDir}\n\n` +
            `Make sure:\n` +
            `1. Python executable exists and is executable\n` +
            `2. Script file exists at the path above\n` +
            `3. All Python dependencies are available`;

        vscode.window.showErrorMessage(errorMsg);
        console.error('Python spawn error:', err);
    });

    child.on('exit', (code, signal) => {
        if (code !== 0 && code !== null) {
            const errorDetails = `Python tool exited with code ${code}\n\n` +
                `Python executable: ${pythonExe}\n` +
                `Script path: ${scriptPath}\n` +
                `Working directory: ${scriptDir}\n\n`;

            let errorOutput = errorDetails;

            if (stderr) {
                errorOutput += `Error output:\n${stderr}\n\n`;
            }

            if (stdout) {
                errorOutput += `Standard output:\n${stdout}\n\n`;
            }

            errorOutput += `\nTroubleshooting:\n` +
                `1. Check if Python script has syntax errors\n` +
                `2. Verify all Python imports are available (tkinter, etc.)\n` +
                `3. Check Developer Console (Help > Toggle Developer Tools) for full details\n` +
                `4. Try running: "${pythonExe}" "${scriptPath}" from command line`;

            vscode.window.showErrorMessage(errorOutput, 'Open Developer Console').then(selection => {
                if (selection === 'Open Developer Console') {
                    vscode.commands.executeCommand('workbench.action.toggleDevTools');
                }
            });

            console.error('Python tool exit details:', {
                code,
                signal,
                stdout,
                stderr,
                pythonExe,
                scriptPath,
                scriptDir
            });
        } else if (code === 0) {
            console.log('Python tool completed successfully');
        }

        if (signal) {
            console.log(`Python tool terminated by signal: ${signal}`);
        }
    });

    // Log for debugging
    console.log(`Launched Python tool: ${scriptPath}`);
    console.log(`Python executable: ${pythonExe}`);
    console.log(`Working directory: ${scriptDir}`);
}

/**
 * Opens the Feature Generator GUI
 */
function openFeatureGenerator(context: vscode.ExtensionContext): void {
    vscode.window.showInformationMessage('Opening Next.js Feature Generator...');
    spawnPythonTool(context, 'generate_feature/generate_feature.py');
}

/**
 * Opens the Translation Extractor GUI
 */
function openTranslationExtractor(context: vscode.ExtensionContext): void {
    vscode.window.showInformationMessage('Opening Translation Key Extractor...');
    spawnPythonTool(context, 'translation_extractor/translation_extractor.py');
}
/**
 * Opens the Postman to Endpoints Converter GUI
 */
function openPostmanToEndpointsConverter(context: vscode.ExtensionContext): void {
    vscode.window.showInformationMessage('Opening Postman to Endpoints Converter...');
    spawnPythonTool(context, 'postman_to_endpoints/main.py');
}

/**
 * This method is called when your extension is activated
 */
export function activate(context: vscode.ExtensionContext): void {
    console.log('Next.js Productivity Tools extension is now active!');

    // Register commands
    const featureGeneratorCommand = vscode.commands.registerCommand(
        'nextjsTools.openFeatureGenerator',
        () => openFeatureGenerator(context)
    );

    const translationExtractorCommand = vscode.commands.registerCommand(
        'nextjsTools.openTranslationExtractor',
        () => openTranslationExtractor(context)
    );
    const postmanToEndpointsConverterCommand = vscode.commands.registerCommand(
        'nextjsTools.openPostmanToEndpointsConverter',
        () => openPostmanToEndpointsConverter(context)
    );

    context.subscriptions.push(featureGeneratorCommand, translationExtractorCommand, postmanToEndpointsConverterCommand);

    // Show welcome message
    vscode.window.showInformationMessage(
        'Next.js Productivity Tools is ready! Use Command Palette to access tools.'
    );
}

/**
 * This method is called when your extension is deactivated
 */
export function deactivate(): void {
    console.log('Next.js Productivity Tools extension is now deactivated');
}
