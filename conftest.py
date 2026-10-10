import pytest
import storage

@pytest.fixture(autouse=True)
def protect_real_data_file(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "data.json")