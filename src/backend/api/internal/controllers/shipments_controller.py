from fastapi import HTTPException

from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

# Internal
from ...internal.repositories import crud
from ..models.models import Shipment, ShipmentCreate


class ShipmentController:
    def __init__(self):
        pass

    def get_shipments(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        carriers: Optional[List[str]] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
    ):
        """
        Retrieves a list of shipments from the database with optional filtering parameters.

        Returns:
            List[Shipment]: A list of shipment objects that match the filtering criteria, serialized to the appropriate model format.
        """
        shipments = crud.get_shipments(
            db,
            skip=skip,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
            carriers=carriers,
            min_price=min_price,
            max_price=max_price,
        )

        shipments_serializable = [
            Shipment.model_validate(shipment) for shipment in shipments
        ]

        return shipments_serializable

    def create_shipment(self, shipment: ShipmentCreate, db: Session):
        """
        Creates a new shipment record in the database.

        Args:
            shipment (ShipmentCreate): The shipment data to create, encapsulated in a ShipmentCreate schema.
            db (Session): Database session.

        Raises:
            HTTPException: Raised if an error occurs while validating the shipment data.
            HTTPException: Raised if a shipment with the same shipment number already exists.
            HTTPException: Raised if there is an error during the creation of the shipment in the database.

        Returns:
            Shipment: The newly created shipment object.
        """

        try:
            db_shipment = crud.get_shipment_by_shipment_number(
                db, shipment_number=shipment.shipment_number
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error while validating the shipment: {e}",
            )

        if db_shipment:
            raise HTTPException(
                status_code=400,
                detail=f"Shipment with number {shipment.shipment_number} already exists.",
            )

        else:
            try:
                created_shipment = crud.create_shipment(db=db, shipment=shipment)
                return created_shipment

            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Error processing shipment: {e}",
                )
