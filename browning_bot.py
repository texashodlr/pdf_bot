#Browning Bot AI

import fitz
import os
import faiss
import numpy as np
import langchain

from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdfs(pdf_folder):
    all_texts = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_folder, filename)
            doc = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            all_texts.append({"filename": filename, "content": text})
            
    return all_texts

def write_files_to_file(directory, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            for file in files:
                f.write(os.path.join(root, file) + '\n ')

def extract_and_save_text(pdf_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    all_texts = []
    
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_folder, filename)
            doc  = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            
            #Saving to a text file
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            with open(os.path.join(output_folder, txt_filename), "w", encoding="utf-8") as f:
                f.write(text)
            
            all_texts.append({"filename": filename, "content": text})
            
    
    return all_texts

pdf_folder = "C:/Users/CDevlin/Documents/pdf_bot/PDFs"

docs = extract_text_from_pdfs(pdf_folder)

#Sanity check to ensure all documents in /PDFs were actually loaded       
print(f"\n\n Loaded {len(docs)} PDF files.\n")
for doc in docs:
    print(f"✔ {doc['filename']} — {len(doc['content'])} characters extracted")
print(f"\n All documents ingested! \n")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

texts = [doc["content"] for doc in docs]

#Saving mappings between index and filenames
metadata = [doc["filename"] for doc in docs]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 100,
)

documents = []
for doc in docs:
    chunks = text_splitter.split_text(doc["content"])
    for i, chunk in enumerate(chunks):
        documents.append(
            Document(
            page_content = chunk,
            metadata = {
                "source": doc["filename"],
                "chunk" : i 
            }
        )
    )

#Chunk checks
print(f"Total document chunks created: {len(documents)}")


embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

faiss_index = FAISS.from_documents(documents, embedding)

#This should match the number of documents loaded in the /PDFs directory
print(f"\n\n FAISS index contains {faiss_index.index.ntotal} vectors.\n")

   
llm = Ollama(model="llama3") #Ollama Is running locally
retriever = faiss_index.as_retriever(search_kwargs={"k":3})

qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

#Asking a Question
while True:
    query = input("\n\n Ask a question about your documents: ")
    if query.lower() in ["exit", "quit"]:
        break
    response = qa_chain.run(query)
    print("→", response,"\n")
    print(f"\nFrom source(s): {[doc.metadata['source'] for doc in retriever.get_relevant_documents(query)]}")
