import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog
import threading
import requests
import json
import os
import re
from datetime import datetime
import shutil


class SandboxAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sandbox AI for Deepseek API")
        self.root.geometry("1000x700")

        self.api_key = self.load_api_key()
        self.conversation_file = "conversation.txt"
        self.code_folder = "CodeSnippets"
        
        # Store conversation history
        self.conversation_history = []

        self.setup_dark_theme()
        self.create_menu()
        self.create_layout()
        
        # Bind Enter key to ask_ai method
        self.bind_enter_key()
        
        # Load existing conversation if any
        self.load_conversation_history()

    # =====================================================
    # DARK MODE
    # =====================================================
    def setup_dark_theme(self):
        self.bg = "#1e1e1e"
        self.fg = "#ffffff"
        self.question_fg = "#000000"
        self.entry_bg = "#2d2d2d"
        self.question_bg = "#ffffd4"  # Lighter background for Question field
        self.root.configure(bg=self.bg)

    # =====================================================
    # LOAD API KEY
    # =====================================================
    def load_api_key(self):
        try:
            if os.path.exists("deepseek.key"):
                with open("deepseek.key", "r") as f:
                    return f.read().strip()
            else:
                # Create an empty key file if it doesn't exist
                with open("deepseek.key", "w") as f:
                    f.write("")
                messagebox.showwarning("Warning", "deepseek.key file created. Please add your API key.")
                return ""
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return ""

    # =====================================================
    # LOAD CONVERSATION HISTORY
    # =====================================================
    def load_conversation_history(self):
        """Load existing conversation from file into history"""
        self.conversation_history = []
        if os.path.exists(self.conversation_file):
            try:
                with open(self.conversation_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # Parse the conversation file to rebuild history
                # This is a simple implementation - you might want to make it more sophisticated
                lines = content.split("\n")
                current_role = None
                current_message = ""
                
                for line in lines:
                    if line.startswith("You: "):
                        if current_role and current_message:
                            self.conversation_history.append({
                                "role": "user" if current_role == "You" else "assistant",
                                "content": current_message.strip()
                            })
                        current_role = "You"
                        current_message = line[5:]
                    elif line.startswith("AI: "):
                        if current_role and current_message:
                            self.conversation_history.append({
                                "role": "user" if current_role == "You" else "assistant",
                                "content": current_message.strip()
                            })
                        current_role = "AI"
                        current_message = line[5:]
                    elif line and not line.startswith("=") and not line.startswith("Time:"):
                        current_message += "\n" + line
                
                # Add the last message
                if current_role and current_message:
                    self.conversation_history.append({
                        "role": "user" if current_role == "You" else "assistant",
                        "content": current_message.strip()
                    })
                    
            except Exception as e:
                print(f"Error loading conversation history: {e}")

    # =====================================================
    # CLEAR HISTORY
    # =====================================================
    def clear_history(self):
        """Clear the conversation history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the conversation history?"):
            self.conversation_history = []
            self.context_box.delete("1.0", tk.END)
            self.context_box.insert(
                tk.END,
                "You are a helpful assistant. Always answer in English."
            )
            self.output_box.delete("1.0", tk.END)
            
            # Clear the conversation file
            try:
                with open(self.conversation_file, 'w', encoding='utf-8') as f:
                    f.write("")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear conversation file: {str(e)}")

    # =====================================================
    # MENU
    # =====================================================
    def create_menu(self):
        menubar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Context File", command=self.load_context_file)
        file_menu.add_command(label="Extract Code Blocks", command=self.extract_code_blocks)
        file_menu.add_separator()
        file_menu.add_command(label="Save Conversation As...", command=self.save_conversation_as)
        file_menu.add_command(label="Clear History", command=self.clear_history)
        file_menu.add_separator()
        file_menu.add_command(label="Add/Replace Deepseek Key", command=self.add_replace_api_key)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # About Menu
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="About", menu=about_menu)

        self.root.config(menu=menubar)

    # =====================================================
    # SHOW ABOUT
    # =====================================================
    def show_about(self):
        about_text = """Sandbox AI for Deepseek API

Developed by Theo Uys 2026

This tool was developed for my own use and to learn how LLMs work. 
It first started as a c# console application and now it is a GUI app written in Python.

Features:
- Chat interface for Deepseek API
- Conversation history maintained
- Context file loading
- Code block extraction
- Conversation saving
- Dark theme interface"""
        
        messagebox.showinfo("About", about_text)

    # =====================================================
    # ADD/REPLACE API KEY
    # =====================================================
    def add_replace_api_key(self):
        # Ask for the new API key
        new_key = simpledialog.askstring(
            "Add/Replace Deepseek API Key",
            "Enter your new Deepseek API key:",
            parent=self.root,
            show="*"  # Hide the key as it's typed
        )
        
        if new_key:
            # Clean the key (remove any whitespace)
            new_key = new_key.strip()
            
            if not new_key:
                messagebox.showwarning("Warning", "API key cannot be empty.")
                return
            
            try:
                # Save the new key to deepseek.key file
                with open("deepseek.key", "w") as f:
                    f.write(new_key)
                
                # Update the current API key in memory
                self.api_key = new_key
                
                # Test the new key
                if self.test_api_key():
                    messagebox.showinfo(
                        "Success", 
                        "API key has been successfully updated and tested!"
                    )
                else:
                    messagebox.showwarning(
                        "Warning", 
                        "API key saved but failed to validate. Please check if the key is correct."
                    )
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save API key: {str(e)}")

    # =====================================================
    # TEST API KEY
    # =====================================================
    def test_api_key(self):
        """Test if the API key is valid by making a simple request"""
        if not self.api_key:
            return False
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Make a simple request to check if the key works
            response = requests.get(
                "https://api.deepseek.com/models",
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception:
            return False

    # =====================================================
    # LAYOUT
    # =====================================================
    def create_layout(self):

        tk.Label(self.root, text="Question", bg=self.bg, fg=self.fg).pack()

        self.prompt_entry = tk.Entry(
            self.root,
            bg=self.question_bg,  # Use lighter background for Question field
            fg=self.question_fg,
            insertbackground="black"
        )
        self.prompt_entry.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.root, text="System Context", bg=self.bg, fg=self.fg).pack()

        self.context_box = scrolledtext.ScrolledText(
            self.root,
            height=5,
            bg=self.entry_bg,
            fg=self.fg,
            insertbackground="white"
        )
        self.context_box.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # Set default system prompt
        self.context_box.insert(
            tk.END,
            "You are a helpful assistant. Always answer in English."
        )

        tk.Label(self.root, text="AI Response", bg=self.bg, fg=self.fg).pack()

        self.output_box = scrolledtext.ScrolledText(
            self.root,
            height=25,
            bg=self.entry_bg,
            fg=self.fg,
            insertbackground="white"
        )
        self.output_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # =====================================================
    # BIND ENTER KEY
    # =====================================================
    def bind_enter_key(self):
        # Bind Enter key to the prompt entry widget
        self.prompt_entry.bind('<Return>', lambda event: self.ask_ai())
        
        # Optional: Also bind Ctrl+Enter for multiline input if you want to allow line breaks
        self.prompt_entry.bind('<Control-Return>', lambda event: self.insert_newline())

    def insert_newline(self):
        # Insert a newline at cursor position
        current_text = self.prompt_entry.get()
        cursor_pos = self.prompt_entry.index(tk.INSERT)
        self.prompt_entry.insert(cursor_pos, '\n')
        return "break"  # Prevents default behavior

    # =====================================================
    # LOAD CONTEXT FILE
    # =====================================================
    def load_context_file(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Replace system context instead of appending
                self.context_box.delete("1.0", tk.END)
                self.context_box.insert(
                    tk.END,
                    content
                )

            except Exception as e:
                messagebox.showerror("Error", str(e))

    # =====================================================
    # SAVE CONVERSATION AS
    # =====================================================
    def save_conversation_as(self):
        # Ask user for filename
        filename = simpledialog.askstring(
            "Save Conversation",
            "Enter filename (without extension):",
            parent=self.root
        )
        
        if filename:
            # Clean the filename
            filename = self.valid_filename(filename.strip())
            
            if not filename:
                messagebox.showwarning("Warning", "Invalid filename")
                return
            
            # Add .txt extension if not present
            if not filename.endswith('.txt'):
                filename += '.txt'
            
            try:
                # Check if current conversation file exists
                if os.path.exists(self.conversation_file):
                    # Copy the conversation file to new name
                    shutil.copy2(self.conversation_file, filename)
                    
                    messagebox.showinfo(
                        "Success",
                        f"Conversation saved as: {filename}\n\n"
                        f"The current conversation remains active."
                    )
                    
                else:
                    messagebox.showwarning(
                        "Warning",
                        "No conversation file found to save."
                    )
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save conversation: {str(e)}")

    # =====================================================
    # ASK AI
    # =====================================================
    def ask_ai(self):
        # Get the prompt before clearing
        prompt_text = self.prompt_entry.get().strip()
        
        # Clear the prompt entry after sending
        self.prompt_entry.delete(0, tk.END)
        
        # Only start AI call if there's actual content
        if prompt_text:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": prompt_text
            })
            
            # Start the AI call in a separate thread
            threading.Thread(target=self.call_ai, args=(prompt_text,)).start()
        
        # Return focus to prompt entry for next question
        self.root.after(100, lambda: self.prompt_entry.focus_set())
        
        # Return "break" to prevent default behavior
        return "break"

    # =====================================================
    # SAVE CONVERSATION
    # =====================================================
    def save_conversation(self, user_prompt, ai_response):
        try:
            with open(self.conversation_file, "a", encoding="utf-8") as f:
                f.write("\n" + "=" * 70 + "\n")
                f.write(f"Time: {datetime.now()}\n")
                f.write(f"You: {user_prompt}\n")
                f.write(f"AI: {ai_response}\n")
        except Exception as e:
            print("Save error:", e)

    # =====================================================
    # VALID FILENAME
    # =====================================================
    def valid_filename(self, name):
        invalid = r'[<>:"/\\|?*]'
        cleaned = re.sub(invalid, "_", name)
        # Also remove leading/trailing spaces and dots
        cleaned = cleaned.strip('. ')
        return cleaned

    # =====================================================
    # EXTRACT CODE BLOCKS WITH REAL FILENAMES
    # =====================================================
    def extract_code_blocks(self):
        try:
            content = self.output_box.get("1.0", tk.END)

            if not os.path.exists(self.code_folder):
                os.makedirs(self.code_folder)

            pattern = r"(\*\*(.*?)\*\*)?\s*```(?:\w+)?\n(.*?)```"
            matches = re.findall(pattern, content, re.DOTALL)

            if not matches:
                messagebox.showinfo("Info", "No code blocks found")
                return

            saved = 0

            for idx, match in enumerate(matches, start=1):
                raw_name = match[1].strip()
                code = match[2].strip()

                if raw_name:
                    filename = self.valid_filename(raw_name)
                else:
                    filename = f"code_{idx}.txt"

                filepath = os.path.join(self.code_folder, filename)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(code)

                saved += 1

            messagebox.showinfo(
                "Done",
                f"Saved {saved} files into {self.code_folder}"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =====================================================
    # CALL AI
    # =====================================================
    def call_ai(self, prompt_text):
        self.output_box.delete("1.0", tk.END)

        system_context = self.context_box.get("1.0", tk.END).strip()

        # Check if API key is set
        if not self.api_key:
            self.output_box.insert(tk.END, "Error: No API key found. Please add your Deepseek API key using the 'Add/Replace Deepseek Key' menu option.")
            return

        # Build messages with full conversation history
        messages = [
            {
                "role": "system",
                "content": system_context if system_context else "You are a helpful assistant. Always answer in English."
            }
        ]
        
        # Add conversation history (excluding the last user message which we'll add separately)
        for msg in self.conversation_history[:-1]:  # Exclude the most recent user message
            messages.append(msg)
        
        # Add the current user message
        messages.append({
            "role": "user",
            "content": prompt_text
        })

        body = {
            "model": "deepseek-chat",
            "messages": messages,
            "stream": True
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        ai_response = ""

        try:
            response = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers=headers,
                json=body,
                stream=True,
                timeout=600
            )

            for line in response.iter_lines():
                if line:
                    decoded = line.decode("utf-8")

                    if decoded.startswith("data: "):
                        data = decoded[6:]

                        if data == "[DONE]":
                            break

                        try:
                            chunk = json.loads(data)
                            content = chunk["choices"][0]["delta"].get("content", "")

                            if content:
                                ai_response += content
                                self.output_box.insert(tk.END, content)
                                self.output_box.see(tk.END)
                                self.root.update()

                        except:
                            pass

            # Add AI response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            self.save_conversation(prompt_text, ai_response)

        except Exception as e:
            self.output_box.insert(tk.END, f"Error: {str(e)}")
            # Remove the user message from history if the call failed
            if self.conversation_history and self.conversation_history[-1]["role"] == "user":
                self.conversation_history.pop()


# =====================================================
# START
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SandboxAI(root)
    root.mainloop()