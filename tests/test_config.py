from documind.config import Settings, get_settings


def test_settings_load_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://test:test@localhost/documind")
    monkeypatch.setenv("NVIDIA_NIM_API_KEY", "test-key")
    monkeypatch.setenv("NVIDIA_NIM_EMBEDDING_MODEL", "test-embedding-model")
    monkeypatch.setenv("NVIDIA_NIM_GENERATION_MODEL", "test-generation-model")

    settings = Settings(_env_file=None)

    assert settings.database_url.startswith("postgresql+psycopg://")
    assert settings.nvidia_nim_api_key == "test-key"
    assert settings.nvidia_nim_base_url == "https://integrate.api.nvidia.com/v1"


def test_get_settings_reads_environment(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://test:test@localhost/documind")
    monkeypatch.setenv("NVIDIA_NIM_API_KEY", "test-key")
    monkeypatch.setenv("NVIDIA_NIM_EMBEDDING_MODEL", "test-embedding-model")
    monkeypatch.setenv("NVIDIA_NIM_GENERATION_MODEL", "test-generation-model")
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.nvidia_nim_generation_model == "test-generation-model"
