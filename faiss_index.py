import faiss
import numpy as np

dimension = embeddings.shaper[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

#Saving mappings between index and filenames
metadata = [doc["filename"] for doc in docs]