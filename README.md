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