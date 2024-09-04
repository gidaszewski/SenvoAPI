from fastapi import APIRouter, HTTPException, status, Depends, Query

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

# Internal
from ..internal.controllers.shipments_controller import (
    Shipment,
    ShipmentCreate,
    ShipmentController,
)

from ..internal.repositories.database import db

router = APIRouter(prefix="/api/v1")
shipment_controller = ShipmentController()


@router.get(
    "/shipments/",
    response_model=List[Shipment],
    status_code=status.HTTP_200_OK,
    summary="Get shipments",
)
def get_shipments(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = Query(None, alias="start-date"),
    end_date: Optional[date] = Query(None, alias="end-date"),
    carriers: Optional[List[str]] = Query(None),
    min_price: Optional[float] = Query(None, alias="min-price"),
    max_price: Optional[float] = Query(None, alias="max-price"),
    db: Session = Depends(db),
):

    # Validate carriers
    if carriers:
        invalid_carriers = [
            carrier
            for carrier in carriers
            if carrier not in ["dhl-express", "fedex", "ups"]
        ]
        if invalid_carriers:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid carriers provided: {invalid_carriers}",
            )
    try:
        return shipment_controller.get_shipments(
            skip=skip,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
            carriers=carriers,
            min_price=min_price,
            max_price=max_price,
            db=db,
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.post(
    "/shipments/",
    response_model=List[ShipmentCreate],
    status_code=status.HTTP_201_CREATED,
    summary="Upload a list of shipments",
)
def post_shipments(shipments: List[ShipmentCreate], db: Session = Depends(db)):

    try:
        shipments_created = [
            shipment_controller.create_shipment(shipment, db=db)
            for shipment in shipments
        ]

        return shipments_created

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
