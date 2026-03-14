# DeepSeek Chat Application

## Overview
A modern web-based chat application powered by DeepSeek's AI models. This application provides an intuitive interface for interacting with DeepSeek's language models, featuring real-time conversations, markdown support, and a clean, responsive design.

## Features

### 🎯 Core Functionality
- **Real-time AI Conversations**: Chat seamlessly with DeepSeek's advanced language models
- **Multiple Model Support**: Switch between different DeepSeek models (default: DeepSeek Chat)
- **Markdown Support**: AI responses are rendered with full markdown formatting including code blocks, lists, and tables
- **Conversation History**: View and manage your chat history in the sidebar
- **Copy to Clipboard**: Easily copy AI responses with a single click

### 🎨 User Interface
- **Clean, Modern Design**: Sleek dark theme with intuitive controls
- **Responsive Layout**: Works perfectly on desktop and mobile devices
- **Sidebar Navigation**: Collapsible sidebar for conversation management
- **Loading Indicators**: Visual feedback during AI processing
- **Error Handling**: User-friendly error messages and recovery options

### 🔧 Technical Features
- **Local Storage**: Conversations are saved locally in your browser
- **API Key Management**: Secure API key storage and management
- **Streaming Responses**: Real-time token streaming for natural conversation flow
- **Code Syntax Highlighting**: Beautifully formatted code blocks with syntax highlighting

## Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- A DeepSeek API key

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd <repository-directory>
   ```

2. **Open the Application**
   Since this is a client-side application, you can simply open the `index.html` file in your web browser:
   ```bash
   # Double-click index.html or use:
   open index.html  # macOS
   start index.html # Windows
   xdg-open index.html # Linux
   ```

3. **Alternative: Local Server (Recommended)**
   For best performance, run a local server:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js with http-server
   npx http-server
   
   # Using PHP
   php -S localhost:8000
   ```
   Then visit `http://localhost:8000` in your browser.

### Obtaining a DeepSeek API Key

1. **Visit DeepSeek Platform**
   Go to [DeepSeek's official platform](https://platform.deepseek.com/)

2. **Create an Account**
   - Sign up for a new account or log in if you already have one
   - Complete any required verification steps

3. **Access API Keys**
   - Navigate to the API section in your dashboard
   - Look for "API Keys" or "Developers" section

4. **Generate New Key**
   - Click "Create new API key"
   - Give your key a descriptive name (e.g., "Web Chat App")
   - Copy the generated API key immediately (you won't be able to see it again)

5. **Set Up in Application**
   - Open the chat application
   - Click the settings/setup button (usually gear icon or in sidebar)
   - Paste your API key in the designated field
   - Save the configuration

### ⚠️ Security Note
- **Never commit your API key** to version control
- The API key is stored locally in your browser's storage
- For production deployment, consider implementing backend proxy for enhanced security

## Usage Guide

### Starting a Conversation
1. Enter your API key in the settings if not already configured
2. Type your message in the input box at the bottom
3. Press Enter or click the send button
4. Wait for the AI response (indicated by typing animation)

### Managing Conversations
- **New Chat**: Click the "+ New Chat" button in the sidebar
- **Switch Conversations**: Click any conversation in the sidebar history
- **Delete Conversations**: Hover over a conversation and click the delete icon
- **Rename Conversations**: Click the edit icon next to conversation names

### Features in Action
- **Code Blocks**: AI automatically formats code with proper syntax highlighting
- **Copy Responses**: Click the copy icon on any AI message to copy it to clipboard
- **Model Switching**: Use the model selector to switch between available DeepSeek models
- **Clear Context**: Start fresh conversations to clear the AI's context

## Project Structure
```
├── index.html          # Main application file
├── README.md           # This documentation
├── assets/            # Static assets (if any)
│   ├── css/          # Stylesheets
│   ├── js/           # JavaScript files
│   └── images/       # Image assets
└── (other project files)
```

## Technical Details

### API Integration
- **Endpoint**: `https://api.deepseek.com/chat/completions`
- **Method**: POST with streaming support
- **Authentication**: Bearer token using your API key
- **Headers**: Standard OpenAI-compatible headers

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Storage
- Uses `localStorage` for persisting conversations and settings
- No data is sent to external servers except DeepSeek API

## Troubleshooting

### Common Issues

1. **"Invalid API Key" Error**
   - Verify your API key is correctly copied
   - Check if the API key has expired or been revoked
   - Ensure you're using the correct DeepSeek platform

2. **Application Not Loading**
   - Check browser console for errors (F12 → Console)
   - Ensure you're serving from a local server for best compatibility
   - Clear browser cache and reload

3. **Slow Responses**
   - Check your internet connection
   - DeepSeek API might be experiencing high load
   - Try reducing the response length in settings

4. **Messages Not Saving**
   - Check if localStorage is enabled in your browser
   - Try in a private/incognito window to rule out extensions

### Getting Help
- Check browser console for detailed error messages
- Verify network tab for API request/response details
- Ensure CORS is properly handled (local server helps with this)

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
Feel free to change and share the code.

## Acknowledgments
- Built with [DeepSeek API](https://platform.deepseek.com/)
- Markdown rendering powered by marked.js
- Icons from [Font Awesome](https://fontawesome.com/)
- Syntax highlighting by highlight.js

## Support
For issues with the application, please open an issue on GitHub. For DeepSeek API issues, contact DeepSeek support through their official platform.

---

**Note**: This application requires an active internet connection and a valid DeepSeek API key to function. API usage may be subject to DeepSeek's terms of service and rate limits.
