# 🎨 Lila Chatbot

**AI-Powered Document Assistant** created at the **Lila Kağıt AI Workshop**

Transform your documents into interactive conversations! Upload PDFs, Word documents, or text files and ask intelligent questions about their content using advanced AI technology.

## 🌟 Features

- 📄 **Smart Document Upload**: Support for PDF, DOCX, and TXT files
- 💬 **Interactive AI Chat**: Ask questions and get intelligent responses
- 🎨 **Beautiful Interface**: Modern Streamlit design with custom styling
- 🔍 **Document Analysis**: Comprehensive content analysis and Q&A
- 🤖 **OpenAI Integration**: Powered by GPT for accurate responses
- 🚀 **Easy Deployment**: One-click deployment to Streamlit Community Cloud

## 🚀 Quick Start

### Local Development

1. **Setup Environment:**
   ```bash
   cd chatbot
   python -m venv chatbot_env
   chatbot_env\Scripts\Activate.ps1  # Windows
   # or
   source chatbot_env/bin/activate  # Mac/Linux
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key:**
   Create a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. **Run the Application:**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open Your Browser:** 
   The app will automatically open at `http://localhost:8501`

## 🌐 Deploy to Streamlit Community Cloud

### Step 1: Prepare Repository
1. Push your code to GitHub
2. Ensure these files are included:
   - `streamlit_app.py`
   - `requirements.txt`
   - `.streamlit/secrets.toml`

### Step 2: Deploy
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Click "New app"
4. Select your repository
5. Set main file: `streamlit_app.py`
6. Add your OpenAI API key in the secrets section
7. Click "Deploy!"

Your **Lila Chatbot** will be live at: `https://your-app-name.streamlit.app`

## 🎯 How to Use

### 📤 Upload Documents
- Use the file uploader in the right column
- Supported formats: PDF, DOCX, TXT
- Multiple files can be uploaded simultaneously
- Files are processed immediately upon upload

### 💬 Chat with Your Documents
- Type questions in the chat input (left column)
- Examples:
  - "What is the main topic of this document?"
  - "Summarize the key points"
  - "What conclusions does the document reach?"
  - "Explain the methodology used"

### 🔍 Manage Documents
- View uploaded documents in expandable sections
- See file size and content preview
- Delete documents using the delete button
- Documents persist during your session

## 🛠️ Technical Details

### Built With
- **Streamlit**: Modern web app framework
- **OpenAI GPT**: Advanced language model
- **PyPDF2**: PDF text extraction
- **python-docx**: Word document processing
- **python-dotenv**: Environment variable management

### System Requirements
- Python 3.7+
- OpenAI API key (optional for basic functionality)
- Internet connection for AI features

### File Limitations
- **File Size**: Recommended < 10MB per file
- **Total Memory**: ~200MB on Streamlit Community Cloud
- **Session Storage**: Files persist only during active session

## 🎨 About Lila Kağıt AI Workshop

This project was created as part of the **Lila Kağıt AI Workshop**, demonstrating the power of combining:
- Document processing technologies
- AI language models
- Modern web frameworks
- Cloud deployment platforms

The workshop showcases how to build practical AI applications that solve real-world document analysis challenges.

## 🔧 Customization

### Branding
Update the app branding by modifying:
- Header styling in `streamlit_app.py`
- Sidebar information
- Color schemes and themes

### Features
Extend functionality by adding:
- Additional file format support
- Advanced document analysis
- User authentication
- Document persistence

## 🆘 Troubleshooting

### Common Issues
1. **API Key Not Found**
   - Add `OPENAI_API_KEY` to `.env` (local) or secrets (cloud)

2. **File Upload Fails**
   - Check file format and size
   - Ensure file is not corrupted

3. **Deployment Issues**
   - Verify `requirements.txt` is complete
   - Check Streamlit Cloud logs for errors

### Getting Help
- Streamlit Documentation: [docs.streamlit.io](https://docs.streamlit.io)
- OpenAI API Docs: [platform.openai.com/docs](https://platform.openai.com/docs)

## 📊 Features Overview

| Feature | Description | Status |
|---------|-------------|---------|
| PDF Upload | Extract text from PDF files | ✅ |
| DOCX Upload | Process Word documents | ✅ |
| TXT Upload | Handle plain text files | ✅ |
| AI Chat | Intelligent Q&A with documents | ✅ |
| Multi-file | Handle multiple documents | ✅ |
| Cloud Deploy | Easy Streamlit Cloud deployment | ✅ |
| Mobile Ready | Responsive design | ✅ |

## 🚀 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] OpenAI API key ready
- [ ] `requirements.txt` updated
- [ ] `.streamlit/secrets.toml` configured
- [ ] Streamlit Cloud account created
- [ ] Repository connected to Streamlit
- [ ] App deployed and tested

## 📄 License

This project is open source and available under the MIT License.

---

**🎨 Created with ❤️ at Lila Kağıt AI Workshop**

*Transforming documents into conversations, one upload at a time!* 