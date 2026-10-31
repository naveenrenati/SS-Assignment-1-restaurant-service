from fastapi import APIRouter
from typing import Optional
from app.models.restaurant import RestaurantCreate, RestaurantUpdate, MenuItemCreate
from app.controllers import restaurant_controller as ctrl

router = APIRouter(prefix="/api/restaurants", tags=["Restaurants"])


@router.post("/", status_code=201)
def create_restaurant(data: RestaurantCreate):
    restaurant = ctrl.create_restaurant(data)
    return {"success": True, "message": "Restaurant registered", "data": restaurant}


@router.get("/")
def list_restaurants(city: Optional[str] = None, cuisine: Optional[str] = None):
    restaurants = ctrl.list_restaurants(city, cuisine)
    return {"success": True, "count": len(restaurants), "data": restaurants}


@router.get("/{restaurant_id}")
def get_restaurant(restaurant_id: str):
    restaurant = ctrl.get_restaurant(restaurant_id)
    return {"success": True, "data": restaurant}


@router.put("/{restaurant_id}")
def update_restaurant(restaurant_id: str, data: RestaurantUpdate):
    restaurant = ctrl.update_restaurant(restaurant_id, data)
    return {"success": True, "message": "Restaurant updated", "data": restaurant}


@router.delete("/{restaurant_id}")
def deactivate_restaurant(restaurant_id: str):
    restaurant = ctrl.deactivate_restaurant(restaurant_id)
    return {"success": True, "message": "Restaurant deactivated", "data": restaurant}


@router.post("/{restaurant_id}/menu", status_code=201)
def add_menu_item(restaurant_id: str, item: MenuItemCreate):
    added = ctrl.add_menu_item(restaurant_id, item)
    return {"success": True, "message": "Menu item added", "data": added}


@router.patch("/{restaurant_id}/menu/{item_id}")
def update_menu_item(restaurant_id: str, item_id: str, data: MenuItemCreate):
    updated = ctrl.update_menu_item(restaurant_id, item_id, data)
    return {"success": True, "message": "Menu item updated", "data": updated}


@router.delete("/{restaurant_id}/menu/{item_id}")
def delete_menu_item(restaurant_id: str, item_id: str):
    result = ctrl.delete_menu_item(restaurant_id, item_id)
    return {"success": True, **result}
