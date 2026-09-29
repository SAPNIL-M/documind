from documind.config import get_settings
from documind.database.session import get_engine, get_session_factory


def test_engine_uses_configured_database_url(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    monkeypatch.setenv("NVIDIA_NIM_API_KEY", "test-key")
    monkeypatch.setenv("NVIDIA_NIM_EMBEDDING_MODEL", "test-embedding-model")
    monkeypatch.setenv("NVIDIA_NIM_GENERATION_MODEL", "test-generation-model")
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    assert str(get_engine().url) == "sqlite:///test.db"
