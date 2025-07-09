import streamlit as st
import os
import tempfile
import PyPDF2
import docx
from openai import OpenAI
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Lila Chatbot",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client
@st.cache_resource
def init_openai_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        return OpenAI(api_key=api_key)
    return None

client = init_openai_client()

# Document processing functions
def extract_text_from_file(uploaded_file):
    """Extract text content from uploaded files"""
    try:
        if uploaded_file.type == "text/plain":
            return str(uploaded_file.read(), "utf-8")
        
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() + '\n'
            return text
        
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Save uploaded file temporarily for python-docx
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
            
            doc = docx.Document(tmp_file_path)
            text = ''
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
            
            # Clean up temporary file
            os.unlink(tmp_file_path)
            return text
            
    except Exception as e:
        st.error(f"Error extracting text from {uploaded_file.name}: {str(e)}")
        return None

def get_ai_response(user_message, document_context):
    """Get AI response using OpenAI API"""
    if not client:
        return "I need an OpenAI API key to provide intelligent responses. Please add your OPENAI_API_KEY to the .env file."
    
    try:
        # Create the full prompt with document context
        if document_context:
            full_prompt = f"Based on the following documents:\n\n{document_context}\n\nUser question: {user_message}\n\nPlease answer the question based on the provided documents."
        else:
            full_prompt = f"User question: {user_message}\n\nNote: No documents have been uploaded yet. Please ask the user to upload documents first if their question is about specific documents."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on uploaded documents. Be concise and cite specific parts of the documents when relevant."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error processing your request: {str(e)}"

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = {}

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'document_context' not in st.session_state:
    st.session_state.document_context = ""

# App header with custom styling
st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; margin: 0;">🎨 Lila Chatbot</h1>
    <p style="color: white; font-size: 18px; margin: 5px 0;"><strong>AI-Powered Document Assistant</strong></p>
    <p style="color: #f0f0f0; font-size: 14px; margin: 0;"><em>Created at Lila Kağıt AI Workshop</em></p>
</div>
""", unsafe_allow_html=True)

st.markdown("Upload documents and ask questions about their content with intelligent AI responses!")

# Create two columns for layout
col1, col2 = st.columns([1, 1])

# Left column - Chat interface
with col1:
    st.header("💬 Chat")
    
    # Chat history container
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.chat_history:
            st.info("👋 Welcome to Lila Chatbot! Upload documents on the right, and I'll help you analyze and answer questions about them.")
        else:
            for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
                # User message
                st.markdown(f"""
                <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 5px 0; text-align: right;">
                    <strong>You:</strong> {user_msg}
                </div>
                """, unsafe_allow_html=True)
                
                # Bot message
                st.markdown(f"""
                <div style="background-color: #f5f5f5; padding: 10px; border-radius: 10px; margin: 5px 0;">
                    <strong>Bot:</strong> {bot_msg}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    user_input = st.text_input("Ask a question about your documents:", key="chat_input", placeholder="What is this document about?")
    
    col_send, col_clear = st.columns([1, 1])
    
    with col_send:
        if st.button("Send", type="primary", use_container_width=True):
            if user_input.strip():
                # Show thinking indicator
                with st.spinner("🤔 Thinking..."):
                    # Get AI response
                    bot_response = get_ai_response(user_input, st.session_state.document_context)
                    
                    # Add to chat history
                    st.session_state.chat_history.append((user_input, bot_response))
                    
                # Clear input by rerunning
                st.rerun()
    
    with col_clear:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# Right column - Document upload
with col2:
    st.header("📄 Document Upload")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    # Process uploaded files
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.documents:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    # Extract text
                    text_content = extract_text_from_file(uploaded_file)
                    
                    if text_content:
                        # Store document
                        st.session_state.documents[uploaded_file.name] = {
                            'content': text_content,
                            'size': uploaded_file.size
                        }
                        
                        # Update document context
                        context_parts = []
                        for filename, doc_data in st.session_state.documents.items():
                            context_parts.append(f"Document: {filename}\nContent: {doc_data['content']}")
                        st.session_state.document_context = "\n\n".join(context_parts)
                        
                        st.success(f"✅ Successfully uploaded: {uploaded_file.name}")
                    else:
                        st.error(f"❌ Failed to process: {uploaded_file.name}")
    
    # Display uploaded documents
    st.markdown("---")
    st.subheader("📚 Uploaded Documents")
    
    if st.session_state.documents:
        for filename, doc_data in st.session_state.documents.items():
            with st.expander(f"📄 {filename}"):
                # Document info
                file_size = doc_data['size'] if 'size' in doc_data else 0
                st.write(f"**Size:** {file_size:,} bytes")
                
                # Preview
                preview_text = doc_data['content'][:300]
                if len(doc_data['content']) > 300:
                    preview_text += "..."
                
                st.write("**Preview:**")
                st.text_area("", preview_text, height=100, disabled=True, key=f"preview_{filename}")
                
                # Delete button
                if st.button(f"🗑️ Delete {filename}", key=f"delete_{filename}"):
                    del st.session_state.documents[filename]
                    
                    # Update document context
                    if st.session_state.documents:
                        context_parts = []
                        for fname, doc_data in st.session_state.documents.items():
                            context_parts.append(f"Document: {fname}\nContent: {doc_data['content']}")
                        st.session_state.document_context = "\n\n".join(context_parts)
                    else:
                        st.session_state.document_context = ""
                    
                    st.success(f"Deleted: {filename}")
                    st.rerun()
    else:
        st.info("No documents uploaded yet. Upload files above to get started!")

# Sidebar with information
st.sidebar.title("🎨 About Lila Chatbot")
st.sidebar.markdown("""
**Lila Chatbot** is an AI-powered document assistant created at the **Lila Kağıt AI Workshop**.

**Features:**
- 📤 Upload PDF, DOCX, and TXT files
- 💬 Ask intelligent questions about your documents
- 🤖 Get AI-powered responses with context
- 🔍 Analyze document content efficiently

**How to use:**
1. Upload documents using the file uploader
2. Ask questions in the chat input
3. Get intelligent responses based on your documents

**Supported formats:**
- PDF (.pdf)
- Word documents (.docx)  
- Text files (.txt)

**Created with ❤️ at Lila Kağıt AI Workshop**
""")

# API key status
if client:
    st.sidebar.success("✅ OpenAI API key configured")
else:
    st.sidebar.warning("⚠️ OpenAI API key not found")
    st.sidebar.markdown("Add your API key to `.env` file:")
    st.sidebar.code("OPENAI_API_KEY=your_key_here")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🎨 **Lila Kağıt AI Workshop**")
st.sidebar.markdown("Made with ❤️ using Streamlit & OpenAI") 