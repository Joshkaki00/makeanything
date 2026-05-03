"""
Text embedding using sentence-transformers.

Default model: nomic-ai/nomic-embed-text-v1.5
- 137M parameters, runs on CPU, no API key required.
- Downloads once from HuggingFace, then fully offline.
- Output dimension: 768.
"""
from typing import List

import numpy as np

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
        ValueError: If texts is empty.
    """
    raise NotImplementedError
