import React, { useState, useRef } from 'react';
import { Upload, Send, FileText, Trash2, MessageCircle } from 'lucide-react';
import { uploadPDF, askQuestion, clearDatabase } from './api';
import './App.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    try {
      const result = await uploadPDF(file);
      setUploadedFile(file.name);
      setMessages([{
        role: 'assistant',
        content: `PDF "${file.name}" uploaded successfully! Created ${result.chunks} chunks. You can now ask questions about the document.`
      }]);
    } catch (error: any) {
      setMessages([{
        role: 'assistant',
        content: `Error uploading PDF: ${error.response?.data?.detail || error.message}`
      }]);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await askQuestion(input);
      setMessages(prev => [...prev, { role: 'assistant', content: response.answer }]);
    } catch (error: any) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${error.response?.data?.detail || error.message}`
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = async () => {
    try {
      await clearDatabase();
      setMessages([]);
      setUploadedFile(null);
      setMessages([{
        role: 'assistant',
        content: 'Database cleared. Please upload a new PDF to start chatting.'
      }]);
    } catch (error: any) {
      console.error('Error clearing database:', error);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="header-left">
            <MessageCircle size={24} />
            <h1>Chat with PDF</h1>
          </div>
          
          <div className="header-right">
            {uploadedFile && (
              <div className="file-info">
                <FileText size={16} />
                <span>{uploadedFile}</span>
              </div>
            )}
            
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleUpload}
              className="file-input"
            />
            
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={isUploading}
              className="upload-btn"
            >
              <Upload size={16} />
              <span>{isUploading ? 'Uploading...' : 'Upload PDF'}</span>
            </button>
            
            {uploadedFile && (
              <button
                onClick={handleClear}
                className="clear-btn"
              >
                <Trash2 size={16} />
                <span>Clear</span>
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <main className="main-content">
        <div className="chat-container">
          
          {/* Messages */}
          <div className="messages-container">
            {messages.length === 0 && (
              <div className="empty-state">
                <FileText size={48} />
                <p>Upload a PDF to start chatting with it!</p>
              </div>
            )}
            
            {messages.map((message, index) => (
              <div
                key={index}
                className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
              >
                <div className="message-content">
                  {message.content}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="message assistant-message">
                <div className="message-content">
                  <div className="typing-indicator">
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input Form */}
          <div className="input-container">
            <form onSubmit={handleSubmit} className="input-form">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={uploadedFile ? "Ask a question about your PDF..." : "Please upload a PDF first"}
                disabled={!uploadedFile || isLoading}
                className="text-input"
              />
              <button
                type="submit"
                disabled={!input.trim() || !uploadedFile || isLoading}
                className="send-btn"
              >
                <Send size={16} />
              </button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;