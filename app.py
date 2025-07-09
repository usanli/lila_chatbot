from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
import PyPDF2
import docx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize OpenAI client (you'll need to set OPENAI_API_KEY in .env file)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Store document contents in memory (in production, use a database)
document_store = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(filepath, filename):
    """Extract text content from uploaded files"""
    extension = filename.rsplit('.', 1)[1].lower()
    
    try:
        if extension == 'txt':
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        
        elif extension == 'pdf':
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text() + '\n'
                return text
        
        elif extension == 'docx':
            doc = docx.Document(filepath)
            text = ''
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
            return text
            
    except Exception as e:
        print(f"Error extracting text from {filename}: {str(e)}")
        return None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from the document
        text_content = extract_text_from_file(filepath, filename)
        
        if text_content:
            # Store the document content
            document_store[filename] = {
                'content': text_content,
                'filename': filename
            }
            return jsonify({
                'message': 'File uploaded successfully',
                'filename': filename,
                'preview': text_content[:500] + ('...' if len(text_content) > 500 else '')
            })
        else:
            return jsonify({'error': 'Failed to extract text from document'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get all document contents for context
    context = ""
    if document_store:
        context = "Based on the following documents:\n\n"
        for filename, doc_data in document_store.items():
            context += f"Document: {filename}\n"
            context += f"Content: {doc_data['content']}\n\n"
    
    try:
        # Create the full prompt with document context
        if context:
            full_prompt = f"{context}\nUser question: {user_message}\n\nPlease answer the question based on the provided documents."
        else:
            full_prompt = f"User question: {user_message}\n\nNote: No documents have been uploaded yet. Please ask the user to upload documents first if their question is about specific documents."
        
        # Call OpenAI API (you can replace this with any other AI service)
        if os.getenv('OPENAI_API_KEY'):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on uploaded documents. Be concise and cite specific parts of the documents when relevant."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=500
            )
            
            bot_response = response.choices[0].message.content
        else:
            # Fallback response when no API key is provided
            if context:
                bot_response = f"I can see you've uploaded documents. Your question was: '{user_message}'. However, I need an OpenAI API key to process your question. Please add your OPENAI_API_KEY to the .env file."
            else:
                bot_response = "Please upload some documents first so I can help answer questions about them."
        
        return jsonify({'response': bot_response})
        
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

@app.route('/documents', methods=['GET'])
def get_documents():
    """Get list of uploaded documents"""
    documents = []
    for filename, doc_data in document_store.items():
        documents.append({
            'filename': filename,
            'preview': doc_data['content'][:200] + ('...' if len(doc_data['content']) > 200 else '')
        })
    return jsonify({'documents': documents})

@app.route('/documents/<filename>', methods=['DELETE'])
def delete_document(filename):
    """Delete a specific document"""
    if filename in document_store:
        del document_store[filename]
        # Also delete the file from disk
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'message': 'Document deleted successfully'})
    return jsonify({'error': 'Document not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000) 