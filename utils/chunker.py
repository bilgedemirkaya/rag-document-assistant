import re

def split_into_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text)

def chunk_text(text, chunk_size=3, overlap=1):
    """ overlapping sentence chunks """
    sentences = split_into_sentences(text)
    chunks = []
    i = 0
    while i < len(sentences):
        chunk = " ".join(sentences[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks
