from pydantic import BaseModel
from datetime import date
from typing import Literal


class ShipmentCreate(BaseModel):
    shipment_number: str
    shipment_date: date = None

    address_line_1: str
    address_line_2: str
    postal_code: str
    city: str
    country_code: str

    package_height: float
    package_width: float
    package_depth: float
    package_weight: float

    price_shipment_service: float
    price_currency: str
    carrier: Literal["dhl-express", "ups", "fedex"]
