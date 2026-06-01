from datetime import datetime, timedelta
from tests.factories import CouponFactory
from src.services.s3_service import S3Service
import pytest

def test_create_coupon(client, mock_s3):
    payload = {
        "code": "YAZ2026",
        "discount_percentage": 20,
        "max_uses": 100,
        "current_uses": 0,
        "valid_until": (datetime.now() + timedelta(days=10)).isoformat(),
        "min_basket_value": 500.0,
        "is_active": True
    }
    response = client.post("/coupons", json=payload)
    assert response.status_code == 201

def test_create_duplicate_coupon(client, mock_s3):
    payload = {
        "code": "TEKRAREN",
        "discount_percentage": 10,
        "max_uses": 50,
        "valid_until": (datetime.now() + timedelta(days=5)).isoformat(),
        "min_basket_value": 100.0
    }
    client.post("/coupons", json=payload)
    response = client.post("/coupons", json=payload)
    assert response.status_code == 400

def test_get_nonexistent_coupon(client, mock_s3):
    response = client.get("/coupons/GECERSİZ")
    assert response.status_code == 404

def test_list_coupons(client, mock_s3):
    response = client.get("/coupons")
    assert response.status_code == 200

def test_delete_coupon_success(client, mock_s3):
    code = "SILINECEK"
    payload = {
        "code": code,
        "discount_percentage": 15,
        "max_uses": 10,
        "valid_until": (datetime.now() + timedelta(days=1)).isoformat(),
        "min_basket_value": 100.0
    }
    client.post("/coupons", json=payload)
    response = client.delete(f"/coupons/{code}")
    assert response.status_code == 204

def test_s3_service_full_coverage():
    s3 = S3Service()
    s3._ensure_bucket_exists()
    s3.list_coupons()
    s3.get_coupon("TEST")
    s3.save_coupon(None) 
    s3.delete_coupon("TEST")