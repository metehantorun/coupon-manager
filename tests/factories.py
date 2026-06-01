from datetime import datetime, timedelta
import factory
from faker import Faker
from src.models import Coupon

fake = Faker()

class CouponFactory(factory.Factory):
    class Meta:
        model = Coupon

    code = factory.LazyAttribute(lambda _: fake.unique.lexify(text="??????").upper() + "2026")
    discount_percentage = factory.LazyAttribute(lambda _: fake.random_int(min=10, max=50))
    max_uses = factory.LazyAttribute(lambda _: fake.random_int(min=5, max=100))
    current_uses = 0
    valid_until = factory.LazyAttribute(lambda _: (datetime.now() + timedelta(days=5)).isoformat().split(".")[0])
    min_basket_value = factory.LazyAttribute(lambda _: float(fake.random_int(min=50, max=500)))
    is_active = True