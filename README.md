# Browning Bot (aka RAG-man)
## What is the Browning Bot (Generally)?
The Browning Bot was born out of a need to consider and source many different types of documents for information related to engineering and acquisitions.  
If the DMOC could build some sort of function to consider the wealth of existing policy information and exisiting DMOC historical knowledge that would reduce a lot of new member on-boarding friction--this is Browning Bot.  
## What is the Browning Bot (Technically)?
The Browning Bot is technically a Retrieval-Augmented Generation (RAG) System. In this specific case is just a method to query a PDF/document database.  
A RAG consists of:  
1. Retriever (performing the vector search over the chunks of PDFs/documents)  
2. Generator (the local LLM or in the Browning Bot case; Ollama)  
  
The general workflow looks like:
Collection of PDFs --> Chunk the PDFs --> Embedding of the Chunks --> Aggregation into a Vector DB --> Querying of the Vector DB --> Retrieving of the relevant vectors --> Feeding vectors into the local LLM --> Answer!  
  
  
## What are embeddings?
From huggingface:  
>"An embedding is a numerical representation of a piece of information, for example, text, documents, images, audio, etc. The representation captures the semantic meaning of what is being embedded..."
  [https://huggingface.co/blog/getting-started-with-embeddings]
  
We're currently using Sentence Transformers [https://www.sbert.net/] and their **all-MiniLM-L6-v2** semantic search model.  
 
The loop looks like this:  
1. PDFs/Documents are chunked (e.g., 500 words/chunk).  
2. Each chunk is passed through the semantic search model to produce a 384-dimensional semantic vector.  
3. Vectors go into a FAISS index.  
4. User then asks a question:  
 - Question is embedded with the same model.  
 - FAISS finds the most similar document chunks using vector distance.  
 - These vectors are passed as context to our selected chat model (e.g., LLaMA 3) via ollama.  
