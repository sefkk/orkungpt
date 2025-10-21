# create_db.py

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
import shutil
from langchain_chroma import Chroma
import glob


DATA_PATH = "data"
CHROMA_PATH = "chroma"

gpt4all_embeddings = GPT4AllEmbeddings(
    model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",
    gpt4all_kwargs={'allow_download': 'True'}
)


def create_vector_db():
    "Creates vector DB from personal PDF files."
    documents = load_documents()
    doc_chunks = split_text(documents)
    save_to_chroma(doc_chunks)

def load_documents():
    "Loads PDF documents from a folder."
    documents = []
    pdf_files = glob.glob(os.path.join(DATA_PATH, "*.pdf"))
    
    for pdf_file in pdf_files:
        print(f"Loading {pdf_file}...")
        loader = PyPDFLoader(pdf_file)
        docs = loader.load()
        documents.extend(docs)
    
    return documents

def split_text(documents: list[Document]):
    "Splits documents into chunks."
    chunks = []
    for doc in documents:
        if "transkript.pdf" in doc.metadata.get("source", "").lower():
            # one chunk for transcript to keep context together 
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=0,
                length_function=len,
                add_start_index=True,
            )
        else:
            # for other documents, use smaller chunks, but with overlap 
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=150,
                length_function=len,
                add_start_index=True,
            )
        doc_chunks = text_splitter.split_documents([doc])
        chunks.extend(doc_chunks)

    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    for i, chunk in enumerate(chunks): 
        print(f"\n--- Chunk {i+1} ---")
        print(chunk.page_content) 
    return chunks

def save_to_chroma(chunks: list[Document]):
    "Clear previous db, and save the new db."
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # create db
    db = Chroma.from_documents(
        chunks, gpt4all_embeddings, persist_directory=CHROMA_PATH
    )
    
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    
if __name__ == "__main__":    
    create_vector_db()