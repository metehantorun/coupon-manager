from datetime import datetime, timedelta
import pytest
import httpx
from playwright.sync_api import sync_playwright

@pytest.fixture
def setup_coupon():
    code = "E2ETEST"
    payload = {
        "code": code,
        "discount_percentage": 20,
        "max_uses": 5,
        "valid_until": (datetime.now() + timedelta(days=1)).isoformat().split(".")[0],
        "min_basket_value": 100.0,
        "is_active": True
    }
    httpx.post("http://localhost:8000/coupons", json=payload)
    return code

def test_e2e_validate_success(setup_coupon):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8000/ui/index.html")
        page.fill("#couponCode", setup_coupon)
        page.fill("#basketValue", "150")
        page.click("#validateBtn")
        page.wait_for_selector("#resultMessage")
        assert "Success: Coupon is valid!" in page.text_content("#resultMessage")
        browser.close()

def test_e2e_validate_min_basket_error(setup_coupon):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8000/ui/index.html")
        page.fill("#couponCode", setup_coupon)
        page.fill("#basketValue", "50")
        page.click("#validateBtn")
        page.wait_for_selector("#resultMessage")
        assert "Error:" in page.text_content("#resultMessage")
        browser.close()

def test_e2e_validate_nonexistent_error():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8000/ui/index.html")
        page.fill("#couponCode", "GECERSIZ_KOD")
        page.fill("#basketValue", "200")
        page.click("#validateBtn")
        page.wait_for_selector("#resultMessage")
        assert "Error:" in page.text_content("#resultMessage")
        browser.close()