import os


class Settings:
    APP_TITLE: str = os.getenv("APP_TITLE", "Shipment Tracking API")
    APP_SUMMARY: str = os.getenv(
        "APP_SUMMARY", "API that stores and provides shipment invoice data"
    )
    APP_VERSION: str = os.getenv("APP_VERSION", "0.0.1")


settings = Settings()
