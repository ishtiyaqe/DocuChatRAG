import re


def clean_text(t: str) -> str:
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def chunk_text(text: str, max_tokens: int = 400, overlap: int = 80):
    # simple token-ish split by words; ~1 token ≈ 0.75 words (rough)
    words = text.split()
    step = max(1, max_tokens - overlap)
    chunks = []
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+max_tokens])
        if chunk:
            chunks.append(clean_text(chunk))
    return chunks