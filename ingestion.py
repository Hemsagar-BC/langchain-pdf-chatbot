import io
import fitz
import pytesseract
from PyPDF2 import PdfReader
from PIL import Image
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_image_text(image_files):
    texts, metadatas = [], []
    for idx, img_file in enumerate(image_files):
        img = Image.open(img_file)
        ocr_text = pytesseract.image_to_string(img)
        if ocr_text.strip():
            texts.append(ocr_text)
            metadatas.append({"page": idx + 1, "source": img_file.name})
    return texts, metadatas

def get_pdf_text(pdf_docs):
    texts, metadatas = [], []
    for pdf in pdf_docs:
        pdf_bytes = io.BytesIO(pdf.read())
        pdf_reader = PdfReader(pdf_bytes)

        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text and page_text.strip():
                texts.append(page_text)
                metadatas.append({"page": page_num + 1, "source": pdf.name})
            else:
                pdf_bytes.seek(0)
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                page_obj = doc[page_num]
                pix = page_obj.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                ocr_text = pytesseract.image_to_string(img)
                if ocr_text.strip():
                    texts.append(ocr_text)
                    metadatas.append({"page": page_num + 1, "source": pdf.name})
    return texts, metadatas

def get_text_chunks(raw_texts, metadatas):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=1750,
        chunk_overlap=60,
        length_function=len
    )
    chunks, new_metas = [], []
    for txt, meta in zip(raw_texts, metadatas):
        split_chunks = text_splitter.split_text(txt)
        chunks.extend(split_chunks)
        new_metas.extend([meta] * len(split_chunks))
    return chunks, new_metas
