"""
Text embedding using sentence-transformers.

Default model: nomic-ai/nomic-embed-text-v1.5
- 137M parameters, runs on CPU, no API key required.
- Downloads once from HuggingFace, then fully offline.
- Output dimension: 768.
"""
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "nomic-ai/nomic-embed-text-v1.5"


def embed_texts(texts: List[str], model_name: str = DEFAULT_MODEL) -> np.ndarray:
    """
    Embed a list of strings using a local sentence-transformer model.

    Args:
        texts: Non-empty list of strings to embed.
        model_name: HuggingFace model identifier.

    Returns:
        np.ndarray of shape (len(texts), embedding_dim).

    Raises:
        ValueError: If texts is empty or contains empty strings.
    """
    # Validate input
    if not texts:
        raise ValueError("texts list cannot be empty")

    if any(not text or not text.strip() for text in texts):
        raise ValueError("texts list cannot contain empty or whitespace-only strings")

    # Load model and encode texts
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts)

    # Ensure output is a 2D numpy array
    return np.asarray(embeddings)
