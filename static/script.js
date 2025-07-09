class DocumentChatbot {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
        this.loadDocuments();
    }

    initializeElements() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.documentList = document.getElementById('documentList');
    }

    attachEventListeners() {
        // Chat functionality
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // File upload functionality
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Drag and drop functionality
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Disable input while processing
        this.messageInput.disabled = true;
        this.sendButton.disabled = true;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';

        // Add loading indicator
        const loadingDiv = this.addMessage('Thinking...', 'bot', true);

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            const data = await response.json();

            // Remove loading indicator
            loadingDiv.remove();

            if (response.ok) {
                this.addMessage(data.response, 'bot');
            } else {
                this.addMessage(`Error: ${data.error}`, 'bot');
            }
        } catch (error) {
            // Remove loading indicator
            loadingDiv.remove();
            this.addMessage(`Error: Failed to send message. ${error.message}`, 'bot');
        }

        // Re-enable input
        this.messageInput.disabled = false;
        this.sendButton.disabled = false;
        this.messageInput.focus();
    }

    addMessage(content, sender, isLoading = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        if (isLoading) {
            contentDiv.innerHTML = `<strong>Bot:</strong> <span class="loading"></span> ${content}`;
        } else {
            const senderLabel = sender === 'user' ? 'You' : 'Bot';
            contentDiv.innerHTML = `<strong>${senderLabel}:</strong> ${content}`;
        }

        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;

        return messageDiv;
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        this.uploadFiles(files);
    }

    handleFileSelect(e) {
        const files = e.target.files;
        this.uploadFiles(files);
    }

    async uploadFiles(files) {
        for (let file of files) {
            await this.uploadSingleFile(file);
        }
    }

    async uploadSingleFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                this.showNotification(`Successfully uploaded: ${data.filename}`, 'success');
                this.loadDocuments(); // Refresh document list
            } else {
                this.showNotification(`Upload failed: ${data.error}`, 'error');
            }
        } catch (error) {
            this.showNotification(`Upload failed: ${error.message}`, 'error');
        }
    }

    async loadDocuments() {
        try {
            const response = await fetch('/documents');
            const data = await response.json();

            if (response.ok) {
                this.displayDocuments(data.documents);
            }
        } catch (error) {
            console.error('Failed to load documents:', error);
        }
    }

    displayDocuments(documents) {
        this.documentList.innerHTML = '';

        if (documents.length === 0) {
            this.documentList.innerHTML = '<p style="color: #6c757d; text-align: center; padding: 20px;">No documents uploaded yet</p>';
            return;
        }

        documents.forEach(doc => {
            const docDiv = document.createElement('div');
            docDiv.className = 'document-item';

            docDiv.innerHTML = `
                <div class="document-name">
                    <span>📄 ${doc.filename}</span>
                    <button class="delete-btn" onclick="chatbot.deleteDocument('${doc.filename}')">×</button>
                </div>
                <div class="document-preview">${doc.preview}</div>
            `;

            this.documentList.appendChild(docDiv);
        });
    }

    async deleteDocument(filename) {
        if (!confirm(`Are you sure you want to delete "${filename}"?`)) {
            return;
        }

        try {
            const response = await fetch(`/documents/${encodeURIComponent(filename)}`, {
                method: 'DELETE',
            });

            const data = await response.json();

            if (response.ok) {
                this.showNotification(`Deleted: ${filename}`, 'success');
                this.loadDocuments(); // Refresh document list
            } else {
                this.showNotification(`Delete failed: ${data.error}`, 'error');
            }
        } catch (error) {
            this.showNotification(`Delete failed: ${error.message}`, 'error');
        }
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `${type}-message`;
        notification.textContent = message;

        // Add to upload area temporarily
        this.uploadArea.insertBefore(notification, this.uploadArea.firstChild);

        // Remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
}

// Initialize the chatbot when the page loads
let chatbot;
document.addEventListener('DOMContentLoaded', () => {
    chatbot = new DocumentChatbot();
}); 