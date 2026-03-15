# Sandbox AI for Deepseek API

A desktop AI chat application built with Python and Tkinter for interacting with the DeepSeek API through a simple graphical interface.

---

## Overview

Sandbox AI is a lightweight desktop tool designed for practical AI interaction, especially for:

* code generation
* technical troubleshooting
* context-based prompting
* conversation history retention
* extracting code snippets into usable files

The project started as a console-based application and evolved into a GUI application for easier daily use.

---

## Features

* Dark theme user interface 🌙
* Live streaming AI responses
* Persistent conversation history
* Load external context files
* Extract code blocks into files
* Save conversations manually
* Secure API key storage
* Automatic conversation continuity

---

## Screenshot

[*Add your application screenshot here*](https://github.com/theouys/sandbox-ai/blob/main/Sandbox-AI.png)

Example:

```text
docs/screenshot.png
```

---

## Requirements

* Python 3.10 or newer
* requests library

Install dependencies:

```bash
pip install requests
```

---

## Running the Application

Start the program with:

```bash
python3 sandbox_ai.py
```

---

## First-Time Setup

On first launch, the application creates:

```text
deepseek.key
```

Add your Deepseek API key through:

```text
File → Add/Replace Deepseek Key
```

or manually place your key inside:

```text
deepseek.key
```

---

## Project Structure

```text
SandboxAI/
│── sandbox_ai.py
│── deepseek.key
│── conversation.txt
│── CodeSnippets/
```

---

## Main Interface

The application contains three working areas:

### Question

Type your prompt here.

Press:

```text
Enter
```

to send.

---

### System Context

Controls AI behavior.

Default:

```text
You are a helpful assistant. Always answer in English.
```

You may replace it with:

```text
You are a senior Linux engineer.
```

---

### AI Response

Displays live streamed responses from the API.

---

## Menu Functions

### File Menu

* Load Context File
* Extract Code Blocks
* Save Conversation As
* Clear History
* Add/Replace Deepseek Key
* Exit

---

### About

Displays application information.

---

## Conversation Storage

All sessions are automatically stored in:

```text
conversation.txt
```

This allows conversation continuity between prompts.

---

## Code Extraction

The program detects markdown code blocks and saves them automatically.

Extract using:

```text
File → Extract Code Blocks
```

Saved into:

```text
CodeSnippets/
```

---

## File Naming Logic

If AI provides:

````text
**backup.sh**
```bash
#!/bin/bash
````

Saved as:

```text
backup.sh
```

If no filename exists:

```text
code_1.txt
```

---

## Recommended Usage

For better technical answers:

Use system context such as:

```text
Answer as a senior Oracle SQL developer.
```

or

```text
Answer as a C# architect.
```

---

## Security Notes

Do not commit:

```text
deepseek.key
```

Recommended `.gitignore`:

```gitignore
deepseek.key
conversation.txt
CodeSnippets/
```

---

## Example .gitignore

```gitignore
deepseek.key
conversation.txt
CodeSnippets/
__pycache__/
```

---

## Future Improvements

Planned enhancements:

* multiline prompt input
* syntax highlighting
* export to markdown
* model selection
* local LLM support
* response search

---

## Author

Developed by Theo Uys

2026

---

## License

Add your preferred license here.

Example:

```text
MIT License
```
