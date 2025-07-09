# Document Chatbot

A web-based chatbot application that allows users to upload documents and ask questions about their content. The interface features a chat area on the left and document upload functionality on the right.

## Features

- 📄 **Document Upload**: Support for PDF, DOCX, and TXT files
- 💬 **Interactive Chat**: Ask questions about uploaded documents
- 🎨 **Modern UI**: Clean, responsive interface with drag-and-drop upload
- 🔍 **Document Management**: View, preview, and delete uploaded documents
- 🤖 **AI Integration**: Uses OpenAI GPT for intelligent responses

## Supported File Types

- PDF (.pdf)
- Microsoft Word (.docx)
- Plain Text (.txt)

## Setup Instructions

### 1. Install Dependencies

Make sure you have Python 3.7+ installed, then run:

```bash
pip install -r requirements.txt
```

### 2. Configure OpenAI API (Optional)

For AI-powered responses, you'll need an OpenAI API key:

1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create an account and generate an API key
3. Copy `.env` to create your environment file
4. Add your API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

**Note**: The application will work without an API key but will provide basic responses.

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## How to Use

1. **Upload Documents**: 
   - Drag and drop files onto the upload area (right side)
   - Or click the upload area to select files
   - Supported formats: PDF, DOCX, TXT

2. **Ask Questions**:
   - Type your questions in the chat input (left side)
   - Press Enter or click Send
   - The bot will analyze your documents and provide relevant answers

3. **Manage Documents**:
   - View uploaded documents in the right panel
   - See preview of document content
   - Delete documents using the × button

## Project Structure

```
chatbot/
├── app.py              # Flask backend server
├── index.html          # Main HTML interface
├── static/
│   ├── style.css       # CSS styles
│   └── script.js       # Frontend JavaScript
├── uploads/            # Uploaded files storage
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create from template)
└── README.md          # This file
```

## API Endpoints

- `GET /` - Serve main interface
- `POST /upload` - Upload document files
- `POST /chat` - Send chat messages
- `GET /documents` - List uploaded documents
- `DELETE /documents/<filename>` - Delete specific document

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Document Processing**: PyPDF2, python-docx
- **AI Integration**: OpenAI GPT-3.5-turbo
- **File Storage**: Local filesystem (uploads/ directory)

## Troubleshooting

### Common Issues

1. **"No module named 'xyz'"**: Run `pip install -r requirements.txt`
2. **Upload fails**: Check file format (PDF, DOCX, TXT only)
3. **No AI responses**: Add OpenAI API key to `.env` file
4. **Port 5000 in use**: Change port in `app.py` (last line)

### Error Messages

- **"No documents uploaded yet"**: Upload documents first before asking questions
- **"Failed to extract text"**: Document may be corrupted or password-protected
- **"OpenAI API key required"**: Add your API key to use AI features

## Security Notes

- Files are stored locally in the `uploads/` directory
- File size limited to 16MB
- Only allowed file extensions are processed
- Document content is stored in memory (restart clears all data)

## Development

To modify the application:

1. **Backend changes**: Edit `app.py`
2. **Frontend styling**: Edit `static/style.css`
3. **Frontend functionality**: Edit `static/script.js`
4. **Interface layout**: Edit `index.html`

## License

This project is open source and available under the MIT License. 