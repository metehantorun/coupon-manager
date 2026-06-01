import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.services.s3_service import S3Service

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def mock_s3(monkeypatch):
    storage = {}
    
    def mock_save(self, coupon):
        storage[coupon.code] = coupon
        return True
        
    def mock_get(self, code):
        return storage.get(code)
        
    def mock_list(self):
        return list(storage.values())
        
    def mock_delete(self, code):
        if code in storage:
            del storage[code]
            return True
        return False

    monkeypatch.setattr(S3Service, "_ensure_bucket_exists", lambda self: None)
    monkeypatch.setattr(S3Service, "save_coupon", mock_save)
    monkeypatch.setattr(S3Service, "get_coupon", mock_get)
    monkeypatch.setattr(S3Service, "list_coupons", mock_list)
    monkeypatch.setattr(S3Service, "delete_coupon", mock_delete)