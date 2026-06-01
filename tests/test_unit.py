from datetime import datetime, timedelta
from tests.factories import CouponFactory

def test_create_coupon(client):
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
    assert response.json()["code"] == "YAZ2026"

def test_create_duplicate_coupon(client):
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

def test_get_nonexistent_coupon(client):
    response = client.get("/coupons/GECERSİZ")
    assert response.status_code == 404

def test_list_coupons(client):
    response = client.get("/coupons")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_coupon_success(client):
    from datetime import datetime, timedelta
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

def test_delete_nonexistent_coupon(client):
    response = client.delete("/coupons/YOK_OLAN")
    assert response.status_code == 404


def test_create_coupon_with_factory(client):
    fake_coupon = CouponFactory()
    payload = {
        "code": fake_coupon.code,
        "discount_percentage": fake_coupon.discount_percentage,
        "max_uses": fake_coupon.max_uses,
        "valid_until": fake_coupon.valid_until.strftime("%Y-%m-%dT%H:%M:%S") if hasattr(fake_coupon.valid_until, "strftime") else str(fake_coupon.valid_until),
        "min_basket_value": fake_coupon.min_basket_value,
        "is_active": fake_coupon.is_active
    }
    response = client.post("/coupons", json=payload)
    assert response.status_code == 201
    assert response.json()["code"] == fake_coupon.code