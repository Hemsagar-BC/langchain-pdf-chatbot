import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import asyncio
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text  


def get_text_chunks(raw_text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=2000,
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

async def get_vectorstore(text_chunks):
    embeddings= GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore= FAISS.from_texts(texts=text_chunks,embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)
    memory= ConversationBufferWindowMemory(memory_key='chat_history',return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def main():
    load_dotenv()  
    st.set_page_config(page_title="Chat with multiple PDF's", page_icon=":books:")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    st.header("Chat with multiple PDF's :books:")
    query = st.text_input("Ask a question about your documents")

    if st.session_state.conversation and query:
     with st.spinner("Generating answer..."):
        response = st.session_state.conversation.run(query)
        st.write(response)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDF's here and click on Process", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                
                raw_text = get_pdf_text(pdf_docs)
            

                text_chunks = get_text_chunks(raw_text)
                
                vectorstore = asyncio.run(get_vectorstore(text_chunks))
                
                st.session_state.conversation= get_conversation_chain(vectorstore)
                st.success("Done")
        

if __name__ == '__main__':
    main()
