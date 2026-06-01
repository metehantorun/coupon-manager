from datetime import datetime, timedelta

def test_validate_coupon_success(client):
    code = "INDİRİM50"
    payload = {
        "code": code,
        "discount_percentage": 50,
        "max_uses": 10,
        "current_uses": 0,
        "valid_until": (datetime.now() + timedelta(days=1)).isoformat(),
        "min_basket_value": 200.0,
        "is_active": True
    }
    client.post("/coupons", json=payload)
    response = client.post(f"/coupons/{code}/validate?basket_value=300.0")
    assert response.status_code == 200
    assert response.json()["valid"] is True
    assert response.json()["discount_amount"] == 150.0

def test_validate_coupon_min_basket_error(client):
    code = "PREMIUM10"
    payload = {
        "code": code,
        "discount_percentage": 10,
        "max_uses": 5,
        "valid_until": (datetime.now() + timedelta(days=2)).isoformat(),
        "min_basket_value": 1000.0
    }
    client.post("/coupons", json=payload)
    response = client.post(f"/coupons/{code}/validate?basket_value=500.0")
    assert response.status_code == 400
    assert "Basket value is below minimum requirement" in response.json()["detail"]

def test_validate_coupon_expired_error(client):
    code = "ESKİODEV"
    payload = {
        "code": code,
        "discount_percentage": 15,
        "max_uses": 5,
        "valid_until": (datetime.now() - timedelta(days=1)).isoformat(),
        "min_basket_value": 50.0
    }
    client.post("/coupons", json=payload)
    response = client.post(f"/coupons/{code}/validate?basket_value=100.0")
    assert response.status_code == 400
    assert "Coupon has expired" in response.json()["detail"]

def test_validate_inactive_coupon(client):
    code = "PASIF2026"
    payload = {
        "code": code,
        "discount_percentage": 20,
        "max_uses": 10,
        "valid_until": (datetime.now() + timedelta(days=1)).isoformat(),
        "min_basket_value": 50.0,
        "is_active": False
    }
    client.post("/coupons", json=payload)
    response = client.post(f"/coupons/{code}/validate?basket_value=100.0")
    assert response.status_code == 400
    assert "Coupon is inactive" in response.json()["detail"]

def test_validate_coupon_usage_limit_reached(client):
    code = "LIMITSIZ"
    payload = {
        "code": code,
        "discount_percentage": 10,
        "max_uses": 1,
        "current_uses": 1,
        "valid_until": (datetime.now() + timedelta(days=1)).isoformat(),
        "min_basket_value": 50.0,
        "is_active": True
    }
    client.post("/coupons", json=payload)
    response = client.post(f"/coupons/{code}/validate?basket_value=100.0")
    assert response.status_code == 400
    assert "Coupon usage limit reached" in response.json()["detail"]