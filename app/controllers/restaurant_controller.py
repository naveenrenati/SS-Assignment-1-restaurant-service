from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from app.database import db
from app.models.restaurant import RestaurantCreate, RestaurantUpdate, MenuItemCreate
from datetime import datetime, timezone

collection = db["restaurants"]


def _serialize(doc: dict) -> dict:
    """Convert ObjectId fields to strings recursively."""
    doc["_id"] = str(doc["_id"])
    for item in doc.get("menu", []):
        item["_id"] = str(item["_id"])
    return doc


def _to_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(status_code=400, detail=f"Invalid id: {id_str}")


# ── Create restaurant ──────────────────────────────────────────
def create_restaurant(data: RestaurantCreate) -> dict:
    doc = data.model_dump()
    doc["isActive"]  = True
    doc["rating"]    = 0.0
    doc["menu"]      = []
    doc["createdAt"] = doc["updatedAt"] = datetime.now(timezone.utc)
    result = collection.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc


# ── List restaurants ───────────────────────────────────────────
def list_restaurants(city: str = None, cuisine: str = None) -> list:
    query = {"isActive": True}
    if city:
        query["address.city"] = {"$regex": city, "$options": "i"}
    if cuisine:
        query["cuisineType"] = {"$regex": cuisine, "$options": "i"}

    docs = list(collection.find(query, {"menu": 0}))
    return [_serialize(d) for d in docs]


# ── Get by id ──────────────────────────────────────────────────
def get_restaurant(restaurant_id: str) -> dict:
    doc = collection.find_one({"_id": _to_object_id(restaurant_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return _serialize(doc)


# ── Update restaurant ──────────────────────────────────────────
def update_restaurant(restaurant_id: str, data: RestaurantUpdate) -> dict:
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    updates["updatedAt"] = datetime.now(timezone.utc)
    result = collection.find_one_and_update(
        {"_id": _to_object_id(restaurant_id)},
        {"$set": updates},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return _serialize(result)


# ── Deactivate ─────────────────────────────────────────────────
def deactivate_restaurant(restaurant_id: str) -> dict:
    result = collection.find_one_and_update(
        {"_id": _to_object_id(restaurant_id)},
        {"$set": {"isActive": False, "updatedAt": datetime.now(timezone.utc)}},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return _serialize(result)


# ── Add menu item ──────────────────────────────────────────────
def add_menu_item(restaurant_id: str, item: MenuItemCreate) -> dict:
    item_doc = item.model_dump()
    item_doc["_id"] = ObjectId()
    result = collection.find_one_and_update(
        {"_id": _to_object_id(restaurant_id)},
        {"$push": {"menu": item_doc}, "$set": {"updatedAt": datetime.now(timezone.utc)}},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    # Return the newly added item
    added = next(i for i in result["menu"] if i["_id"] == item_doc["_id"])
    added["_id"] = str(added["_id"])
    return added


# ── Update menu item ───────────────────────────────────────────
def update_menu_item(restaurant_id: str, item_id: str, data: MenuItemCreate) -> dict:
    updates = {f"menu.$.{k}": v for k, v in data.model_dump().items() if v is not None}
    updates["updatedAt"] = datetime.now(timezone.utc)
    result = collection.find_one_and_update(
        {
            "_id":      _to_object_id(restaurant_id),
            "menu._id": _to_object_id(item_id)
        },
        {"$set": updates},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Restaurant or menu item not found")
    updated = next((i for i in result["menu"] if str(i["_id"]) == item_id), None)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu item not found")
    updated["_id"] = str(updated["_id"])
    return updated


# ── Delete menu item ───────────────────────────────────────────
def delete_menu_item(restaurant_id: str, item_id: str) -> dict:
    result = collection.find_one_and_update(
        {"_id": _to_object_id(restaurant_id)},
        {
            "$pull": {"menu": {"_id": _to_object_id(item_id)}},
            "$set":  {"updatedAt": datetime.now(timezone.utc)}
        },
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"message": "Menu item removed"}
