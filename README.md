📚 RAG Chatbot – Chat with PDFs & Images

⚡ An intelligent RAG (Retrieval-Augmented Generation) chatbot built with Streamlit, Gemini Pro, FAISS, and HuggingFace embeddings.
Upload your PDFs & Images, and ask questions in natural language – the bot extracts, chunks, embeds, and retrieves answers with sources.

✨ Features

✅ Upload PDFs and extract clean text (OCR fallback for scanned docs)
✅ Upload Images and extract text using Tesseract OCR
✅ Smart text chunking for better context understanding
✅ FAISS vector search for lightning-fast retrieval
✅ Gemini Pro LLM for conversational answers
✅ Shows sources with page numbers for transparency
✅ Interactive chat-like interface with memory

## 📋 Prerequisites

- 🔑 Google Gemini API key → [GET YOUR KEY](https://developers.google.com/)
- 🧰 Tesseract OCR installed (for image/PDF OCR):
  - **Windows:** [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki)
  - **Linux:** `sudo apt install tesseract-ocr`  
  - **Mac:** `brew install tesseract

## 🖥️Setup Instructions

Follow these steps to set up the project:

1. **Clone the repository:**
```bash
git clone https://github.com/Hemsagar-BC/langchain-pdf-chatbot.git
cd rag-chatbot


