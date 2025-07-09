# Document Chatbot - Streamlit Version

A web-based chatbot application built with Streamlit that allows users to upload documents and ask questions about their content. Perfect for deployment on Streamlit Community Cloud!

## 🌟 Features

- 📄 **Document Upload**: Support for PDF, DOCX, and TXT files
- 💬 **Interactive Chat**: Real-time chat with document-aware AI
- 🎨 **Modern UI**: Clean, responsive Streamlit interface
- 🔍 **Document Management**: View, preview, and delete uploaded documents
- 🤖 **AI Integration**: Powered by OpenAI GPT for intelligent responses
- 🚀 **Easy Deployment**: One-click deployment to Streamlit Community Cloud

## 🚀 Quick Start

### Local Development

1. **Clone and setup:**
   ```bash
   cd chatbot
   python -m venv chatbot_env
   chatbot_env\Scripts\Activate.ps1  # Windows
   pip install -r requirements.txt
   ```

2. **Configure OpenAI API (Optional):**
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

3. **Run the application:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser:** The app will automatically open at `http://localhost:8501`

## 🌐 Deploy to Streamlit Community Cloud

### Step 1: Prepare Your Repository

1. **Push to GitHub:**
   - Make sure your code is in a GitHub repository
   - Include these files:
     - `streamlit_app.py` (main app)
     - `requirements.txt` (dependencies)
     - `.streamlit/secrets.toml` (for API key - see below)

2. **Add your API key to Streamlit secrets:**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your_api_key_here"
   ```

### Step 2: Deploy

1. **Visit [share.streamlit.io](https://share.streamlit.io)**
2. **Connect your GitHub account**
3. **Click "New app"**
4. **Select your repository and branch**
5. **Set main file path:** `streamlit_app.py`
6. **Click "Deploy!"**

Your app will be live at: `https://your-app-name.streamlit.app`

## 📁 Project Structure

```
chatbot/
├── streamlit_app.py       # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Local environment variables (not committed)
├── .streamlit/
│   └── secrets.toml      # Streamlit secrets for deployment
├── app.py                # Old Flask version (can be removed)
├── index.html           # Old HTML (can be removed)
├── static/              # Old static files (can be removed)
└── README_streamlit.md  # This file
```

## 🔧 Usage

### Upload Documents
- Use the file uploader in the right column
- Drag & drop or click to select files
- Supported formats: PDF, DOCX, TXT
- Multiple files can be uploaded at once

### Chat with Documents
- Type questions in the chat input (left column)
- Ask about document content, summaries, key points
- The AI will provide context-aware responses
- Chat history is maintained during your session

### Manage Documents
- View uploaded documents in expandable sections
- See file size and content preview
- Delete documents using the delete button
- Documents persist until you refresh or restart

## ⚙️ Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for AI responses

### Streamlit Configuration

You can customize the app by modifying `streamlit_app.py`:

- **Page layout**: Change `layout="wide"` to `layout="centered"`
- **Theme**: Streamlit will use your system theme by default
- **Sidebar**: Modify `initial_sidebar_state` to "collapsed" or "expanded"

## 🔍 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Add your API key to `.env` file locally
   - Add your API key to `.streamlit/secrets.toml` for deployment

2. **File upload fails**
   - Check file format (PDF, DOCX, TXT only)
   - Ensure file is not corrupted or password-protected

3. **App doesn't load on Streamlit Cloud**
   - Check that `requirements.txt` is in the root directory
   - Verify `streamlit_app.py` path is correct
   - Check deployment logs for errors

### Getting Help

- Check Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
- OpenAI API documentation: [platform.openai.com/docs](https://platform.openai.com/docs)

## 🆚 Streamlit vs Flask Version

| Feature | Streamlit | Flask |
|---------|-----------|-------|
| **Deployment** | ✅ One-click deploy | ❌ Requires hosting setup |
| **UI Development** | ✅ Built-in components | ❌ Custom HTML/CSS/JS |
| **Real-time Updates** | ✅ Automatic | ❌ Manual refresh |
| **Session Management** | ✅ Built-in | ❌ Manual implementation |
| **Community Cloud** | ✅ Free hosting | ❌ Need external hosting |

## 📊 Features Comparison

### ✅ What's New in Streamlit Version:
- Easier deployment to Streamlit Community Cloud
- Built-in file upload with progress indicators
- Real-time chat interface with message styling
- Automatic session state management
- Responsive column layout
- Built-in error handling and user feedback
- Sidebar with app information and API key status

### 📱 Interface Layout:
- **Left Column**: Chat interface with message history
- **Right Column**: File upload and document management
- **Sidebar**: App information and settings

## 🎯 Next Steps

1. **Test locally** with `streamlit run streamlit_app.py`
2. **Push to GitHub** repository
3. **Deploy to Streamlit Community Cloud**
4. **Share your app** with others!

## 📄 License

This project is open source and available under the MIT License.

---

**Happy chatting with your documents! 🤖📚** 