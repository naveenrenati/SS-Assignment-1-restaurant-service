import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes.restaurant_routes import router as restaurant_router

load_dotenv()

app = FastAPI(
    title="Restaurant Service",
    description="Manages restaurant profiles and menus — Online Food Ordering System",
    version="1.0.0"
)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "UP",
        "service": "restaurant-service"
    }


app.include_router(restaurant_router)
