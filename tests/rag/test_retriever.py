"""
Tests for src/rag/retriever.py

All tests FAIL until retrieve is implemented.
"""
import pytest

from src.rag.retriever import retrieve


class TestInputValidation:
    def test_empty_query_raises_value_error(self, mocker):
        mock_store = mocker.MagicMock()
        with pytest.raises(ValueError, match="empty"):
            retrieve("", store=mock_store)

    def test_whitespace_query_raises_value_error(self, mocker):
        mock_store = mocker.MagicMock()
        with pytest.raises(ValueError):
            retrieve("   ", store=mock_store)


class TestRetrieval:
    def test_returns_list(self, mocker):
        mock_store = mocker.MagicMock()
        mock_store.query.return_value = []
        result = retrieve("how do I use Docker", store=mock_store, rerank=False)
        assert isinstance(result, list)

    def test_empty_store_returns_empty_list(self, mocker):
        mock_store = mocker.MagicMock()
        mock_store.query.return_value = []
        result = retrieve("how do I containerize my app", store=mock_store, rerank=False)
        assert result == []
