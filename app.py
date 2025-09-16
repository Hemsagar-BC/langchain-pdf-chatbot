import streamlit as st
import asyncio
from dotenv import load_dotenv

from ingestion import get_pdf_text, get_image_text, get_text_chunks
from embeddings_model import get_vectorstore
from conversation import get_conversation_chain

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with PDFs & Images", page_icon=":books:")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.header("Chat with PDFs & Images :books:")

    with st.sidebar:
        st.subheader("Your documents")
        uploaded_pdfs = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
        uploaded_images = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

        if st.button("Process"):
            with st.spinner("Processing..."):
                all_texts, all_metas = [], []
                if uploaded_pdfs:
                    texts, metas = get_pdf_text(uploaded_pdfs)
                    all_texts.extend(texts); all_metas.extend(metas)
                if uploaded_images:
                    texts, metas = get_image_text(uploaded_images)
                    all_texts.extend(texts); all_metas.extend(metas)

                if all_texts:
                    text_chunks, chunk_metas = get_text_chunks(all_texts, all_metas)
                    vectorstore = asyncio.run(get_vectorstore(text_chunks, chunk_metas))
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.success("Processing complete!")
                else:
                    st.warning("No text could be extracted.")

    # Chat messages
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
        st.chat_message(role).write(msg["content"])
        if msg.get("sources"):
            with st.expander("View Sources"):
                for src in msg["sources"]:
                    st.write(f"📄 {src['source']} — Page {src['page']}")

    # Input
    if query := st.chat_input("Type your message..."):
        if st.session_state.conversation is None:
            st.warning("Please upload and process documents first!")
        else:
            st.chat_message("user").write(query)
            st.session_state.messages.append({"role": "user", "content": query})
            with st.spinner("Thinking..."):
                result = st.session_state.conversation({"question": query})
            answer = result["answer"]
            sources = result.get("source_documents", [])
            source_list = [{"page": doc.metadata.get("page", "?"), "source": doc.metadata.get("source", "unknown file")} for doc in sources]

            st.chat_message("assistant").write(answer)
            if source_list:
                with st.expander("View Sources"):
                    for src in source_list:
                        st.write(f"📄 {src['source']} — Page {src['page']}")
            st.session_state.messages.append({"role": "assistant", "content": answer, "sources": source_list})

if __name__ == "__main__":
    main()
