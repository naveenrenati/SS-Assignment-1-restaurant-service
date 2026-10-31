from fastapi import APIRouter
from typing import Optional
from app.models.restaurant import RestaurantCreate, RestaurantUpdate, MenuItemCreate
from app.controllers import restaurant_controller as ctrl

router = APIRouter(tags=["Restaurants"])


@router.post("/api/restaurants", status_code=201)
@router.post("/api/restaurants/", status_code=201, include_in_schema=False)
def create_restaurant(data: RestaurantCreate):
    restaurant = ctrl.create_restaurant(data)
    return {"success": True, "message": "Restaurant registered", "data": restaurant}


@router.get("/api/restaurants")
@router.get("/api/restaurants/", include_in_schema=False)
def list_restaurants(city: Optional[str] = None, cuisine: Optional[str] = None):
    restaurants = ctrl.list_restaurants(city, cuisine)
    return {"success": True, "count": len(restaurants), "data": restaurants}


@router.get("/api/restaurants/{restaurant_id}")
def get_restaurant(restaurant_id: str):
    restaurant = ctrl.get_restaurant(restaurant_id)
    return {"success": True, "data": restaurant}


@router.put("/api/restaurants/{restaurant_id}")
def update_restaurant(restaurant_id: str, data: RestaurantUpdate):
    restaurant = ctrl.update_restaurant(restaurant_id, data)
    return {"success": True, "message": "Restaurant updated", "data": restaurant}


@router.delete("/api/restaurants/{restaurant_id}")
def deactivate_restaurant(restaurant_id: str):
    restaurant = ctrl.deactivate_restaurant(restaurant_id)
    return {"success": True, "message": "Restaurant deactivated", "data": restaurant}


@router.post("/api/restaurants/{restaurant_id}/menu", status_code=201)
def add_menu_item(restaurant_id: str, item: MenuItemCreate):
    added = ctrl.add_menu_item(restaurant_id, item)
    return {"success": True, "message": "Menu item added", "data": added}


@router.patch("/api/restaurants/{restaurant_id}/menu/{item_id}")
def update_menu_item(restaurant_id: str, item_id: str, data: MenuItemCreate):
    updated = ctrl.update_menu_item(restaurant_id, item_id, data)
    return {"success": True, "message": "Menu item updated", "data": updated}


@router.delete("/api/restaurants/{restaurant_id}/menu/{item_id}")
def delete_menu_item(restaurant_id: str, item_id: str):
    result = ctrl.delete_menu_item(restaurant_id, item_id)
    return {"success": True, **result}
