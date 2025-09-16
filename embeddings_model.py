from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

async def get_vectorstore(text_chunks, metadatas):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    vectorstore = FAISS.from_texts(
        texts=text_chunks,
        embedding=embeddings,
        metadatas=metadatas
    )
    return vectorstore
