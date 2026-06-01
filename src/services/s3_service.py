import json
import os
from typing import Optional
import boto3
from botocore.exceptions import ClientError
from ..models import Coupon

class S3Service:
    def __init__(self):
        self.endpoint_url = os.getenv("S3_ENDPOINT_URL", "http://localstack:4566")
        self.s3 = boto3.resource(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1"
        )
        self.bucket_name = "coupon-vault"
        self.bucket = self.s3.Bucket(self.bucket_name)
        self.bucket_exists = False  

    def _ensure_bucket_exists(self):
        if not self.bucket_exists:
            try:
                self.bucket.create()
                self.bucket_exists = True
            except ClientError:
                self.bucket_exists = True 

    def save_coupon(self, coupon: Coupon) -> bool:
        self._ensure_bucket_exists() 
        try:
            self.bucket.put_object(
                Key=f"{coupon.code}.json",
                Body=coupon.model_dump_json()
            )
            return True
        except ClientError:
            return False

    def get_coupon(self, code: str) -> Optional[Coupon]:
        self._ensure_bucket_exists()
        try:
            obj = self.s3.Object(self.bucket_name, f"{code}.json")
            data = json.loads(obj.get()["Body"].read().decode("utf-8"))
            return Coupon(**data)
        except ClientError:
            return None

    def list_coupons(self) -> list[Coupon]:
        self._ensure_bucket_exists()
        coupons = []
        try:
            for obj in self.bucket.objects.all():
                if obj.key.endswith(".json"):
                    code = obj.key.replace(".json", "")
                    coupon = self.get_coupon(code)
                    if coupon:
                        coupons.append(coupon)
        except ClientError:
            pass
        return coupons

    def delete_coupon(self, code: str) -> bool:
        self._ensure_bucket_exists()
        try:
            self.s3.Object(self.bucket_name, f"{code}.json").delete()
            return True
        except ClientError:
            return False