from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Coupon(BaseModel):
    code: str
    discount_percentage: int
    max_uses: int
    current_uses: int = 0
    valid_until: datetime
    min_basket_value: float
    is_active: bool = True