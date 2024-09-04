import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status


import sys

sys.path.append("..")
from backend.bin.main import app


# Testing GET method using query parameter
@pytest.mark.asyncio
async def test_get_performance():
    """GWT:
    GIVEN a shipment database with entries
    WHEN requesting a GET with a limit query parameter
    THEN expect a successful response with a maximum number of results equal to the limit
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/shipments/?limit=2")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) <= 2


# Testing GET method including more than one query parameter at the same time
@pytest.mark.asyncio
async def test_get_with_querys_performance():
    """GWT:
    GIVEN a shipment database with various entries and queryable attributes
    WHEN requesting a GET with multiple query parameters (limit, min-price, carrier)
    THEN expect a successful response filtered by all provided query parameters"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/shipments/?limit=5&min-price=20&carrier=ups")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) <= 5


# Testing POST method
@pytest.mark.asyncio
async def test_post_performance():
    """GWT:
    GIVEN an empty or initialized shipment database
    WHEN submitting a POST request with valid shipment data
    THEN expect a successful creation of the shipment and a response with the created shipment details
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "shipment_number": "282828280",
            "shipment_date": "2024-09-28",
            "address_line_1": "Test Street",
            "address_line_2": "Suite 100",
            "postal_code": "12345",
            "city": "Test City",
            "country_code": "TC",
            "package_height": 10.5,
            "package_width": 20.3,
            "package_depth": 15.2,
            "package_weight": 200.0,
            "price_shipment_service": 19.99,
            "price_currency": "EUR",
            "carrier": "ups",
        }

        response = await ac.post("/api/v1/shipments/", json=[payload])
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.json()) == 1
        assert response.json()[0]["shipment_number"] == "282828280"


# Testing POST method validation
@pytest.mark.asyncio
async def test_error_post_performance():
    """GWT:
    GIVEN a shipment database with an existing shipment number
    WHEN submitting a POST request with a duplicate shipment number
    THEN expect a 400 Bad Request response indicating the shipment already exists"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "shipment_number": "282828280",
            "shipment_date": "2024-09-28",
            "address_line_1": "Test Street",
            "address_line_2": "Suite 100",
            "postal_code": "12345",
            "city": "Test City",
            "country_code": "TC",
            "package_height": 10.5,
            "package_width": 20.3,
            "package_depth": 15.2,
            "package_weight": 200.0,
            "price_shipment_service": 19.99,
            "price_currency": "EUR",
            "carrier": "ups",
        }

        response = await ac.post("/api/v1/shipments/", json=[payload])
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.json()["detail"]
            == "Shipment with number 282828280 already exists."
        )
