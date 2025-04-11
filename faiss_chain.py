from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document

#Wrap FAISS and LangChain together
faiss_index = FAISS(embedding_function=None, index=index, documents=[Document(page_content=doc["content"], metadata={"source": doc["filename"]})
    for doc in docs
])
   
llm = Ollama(model="llama3") #Ollama Is running locally
retriever = faiss_index.as_retriever(search_kwargs={"k":3})

qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

#Asking a Question
query = "QUESTION"
response = qa_chain.run(query)
print(response)