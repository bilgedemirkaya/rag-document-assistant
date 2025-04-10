from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def retrieve_top_k(query_embedding, chunk_embeddings, chunks, k=3):
    sims = cosine_similarity([query_embedding], chunk_embeddings)[0]
    top_indices = np.argsort(sims)[-k:][::-1]
    return [(chunks[i], sims[i]) for i in top_indices]
