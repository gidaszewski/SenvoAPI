from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint

from .database import Base


class Shipment(Base):
    __tablename__ = "Shipments"
    id = Column(Integer, primary_key=True)

    shipment_number = Column(String, unique=True, index=True, key="Tracking Number")
    shipment_date = Column(DateTime, key="Date")

    address_line_1 = Column(String, nullable=False)
    address_line_2 = Column(String)
    postal_code = Column(String(10), nullable=False)
    city = Column(String(80), nullable=False)
    country_code = Column(String(10), nullable=False)

    package_height = Column(Float, nullable=False)
    package_width = Column(Float, nullable=False)
    package_depth = Column(Float, nullable=False)
    package_weight = Column(Float, nullable=False)

    price_shipment_service = Column(Float, nullable=False, key="price")
    price_currency = Column(String(20), nullable=False)
    carrier = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint("package_height > 0", name="check_package_height_positive"),
        CheckConstraint("package_width > 0", name="check_package_width_positive"),
        CheckConstraint("package_depth > 0", name="check_package_depth_positive"),
        CheckConstraint("package_weight > 0", name="check_package_weight_positive"),
        CheckConstraint("price_shipment_service > 0", name="check_price_positive"),
    )
