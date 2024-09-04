from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from typing import List, Optional
from datetime import date

# Internal
from . import models
from .schemas import ShipmentCreate


def get_shipments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    carriers: Optional[List[str]] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    query = db.query(models.Shipment)

    filters = []

    if start_date:
        filters.append(models.Shipment.shipment_date >= start_date)
    if end_date:
        filters.append(models.Shipment.shipment_date <= end_date)
    if carriers:
        filters.append(models.Shipment.carrier.in_(carriers))
    if min_price:
        filters.append(models.Shipment.price_shipment_service >= min_price)
    if max_price:
        filters.append(models.Shipment.price_shipment_service <= max_price)

    if filters:
        query = query.filter(and_(*filters))

    return query.offset(skip).limit(limit).all()


def create_shipment(db: Session, shipment: ShipmentCreate):
    try:
        db_shipment = models.Shipment(**shipment.model_dump())
        db.add(db_shipment)
        db.commit()
        db.refresh(db_shipment)
        return db_shipment
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"The following object contains invalid data: {str(e.orig)}",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


def get_shipment_by_shipment_number(db: Session, shipment_number: str):
    return (
        db.query(models.Shipment)
        .filter(models.Shipment.shipment_number == shipment_number)
        .first()
    )
