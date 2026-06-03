from fastapi import FastAPI, HTTPException, status, Query
from typing import List
from datetime import datetime
from .models import Coupon
from .services.s3_service import S3Service
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Coupon Discount Manager API")
app.mount("/ui", StaticFiles(directory="src/static"), name="static")
Instrumentator().instrument(app).expose(app)
s3_service = S3Service()

@app.post("/coupons", response_model=Coupon, status_code=status.HTTP_201_CREATED)
def create_coupon(coupon: Coupon):
    existing = s3_service.get_coupon(coupon.code)
    if existing:
        raise HTTPException(status_code=400, detail="Coupon code already exists")
    success = s3_service.save_coupon(coupon)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save coupon to cloud storage")
    return coupon

@app.get("/coupons", response_model=List[Coupon])
def list_coupons():
    return s3_service.list_coupons()

@app.get("/coupons/{code}", response_model=Coupon)
def get_coupon(code: str):
    coupon = s3_service.get_coupon(code)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return coupon

@app.post("/coupons/{code}/validate")
def validate_coupon(code: str, basket_value: float = Query(..., description="Sepet tutarı")):
    coupon = s3_service.get_coupon(code)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    if not coupon.is_active:
        raise HTTPException(status_code=400, detail="Coupon is inactive")
        
    if datetime.now() > coupon.valid_until:
        raise HTTPException(status_code=400, detail="Coupon has expired")
        
    if basket_value < coupon.min_basket_value:
        raise HTTPException(status_code=400, detail="Basket value is below minimum requirement")
        
    if coupon.current_uses >= coupon.max_uses:
        raise HTTPException(status_code=400, detail="Coupon usage limit reached")
        
    discount_amount = (basket_value * coupon.discount_percentage) / 100
    new_basket_value = basket_value - discount_amount
    
    coupon.current_uses += 1
    s3_service.save_coupon(coupon)
    
    return {
        "valid": True,
        "discount_percentage": coupon.discount_percentage,
        "discount_amount": discount_amount,
        "new_basket_value": new_basket_value
    }

@app.delete("/coupons/{code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coupon(code: str):
    coupon = s3_service.get_coupon(code)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    s3_service.delete_coupon(code)
    return None