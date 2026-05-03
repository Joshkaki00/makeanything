"""
Tests for src/rag/embedder.py

All tests FAIL until embed_texts is implemented.
Note: these tests do NOT load the actual model (slow, requires download).
They are marked to run only when the model is available, or mock the model.

For fast CI: mock the SentenceTransformer.
For full integration: run with --integration flag (add to conftest if needed).
"""
import pytest
import numpy as np

from src.rag.embedder import embed_texts


class TestInputValidation:
    def test_empty_list_raises_value_error(self):
        with pytest.raises(ValueError, match="empty"):
            embed_texts([])

    def test_list_with_empty_string_raises_value_error(self):
        with pytest.raises(ValueError):
            embed_texts([""])


class TestOutputShape:
    def test_single_text_returns_2d_array(self, mocker):
        """Shape should be (1, embedding_dim)."""
        mock_model = mocker.patch("src.rag.embedder.SentenceTransformer")
        mock_model.return_value.encode.return_value = np.zeros((1, 768))
        result = embed_texts(["hello world"])
        assert result.ndim == 2
        assert result.shape[0] == 1

    def test_n_texts_returns_n_rows(self, mocker):
        mock_model = mocker.patch("src.rag.embedder.SentenceTransformer")
        mock_model.return_value.encode.return_value = np.zeros((3, 768))
        result = embed_texts(["a", "b", "c"])
        assert result.shape[0] == 3

    def test_all_rows_same_dimension(self, mocker):
        mock_model = mocker.patch("src.rag.embedder.SentenceTransformer")
        mock_model.return_value.encode.return_value = np.zeros((2, 768))
        result = embed_texts(["short", "a much longer sentence with more words"])
        assert result[0].shape == result[1].shape
