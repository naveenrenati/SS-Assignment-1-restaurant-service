from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from enum import Enum


class MenuCategory(str, Enum):
    STARTER     = "STARTER"
    MAIN_COURSE = "MAIN_COURSE"
    DESSERT     = "DESSERT"
    BEVERAGE    = "BEVERAGE"
    SNACK       = "SNACK"


class Address(BaseModel):
    street:  str
    city:    str
    pincode: str


class OpeningHours(BaseModel):
    open:  str = "09:00"
    close: str = "22:00"


# ── Menu Item ──────────────────────────────────────────────────
class MenuItemCreate(BaseModel):
    name:        str
    description: Optional[str] = None
    price:       float
    category:    MenuCategory
    available:   bool = True


class MenuItemResponse(MenuItemCreate):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True


# ── Restaurant ─────────────────────────────────────────────────
class RestaurantCreate(BaseModel):
    name:          str
    description:   Optional[str] = None
    cuisineType:   str
    address:       Address
    contactNumber: str
    email:         str
    openingHours:  OpeningHours = OpeningHours()


class RestaurantUpdate(BaseModel):
    name:          Optional[str]          = None
    description:   Optional[str]          = None
    cuisineType:   Optional[str]          = None
    address:       Optional[Address]      = None
    contactNumber: Optional[str]          = None
    email:         Optional[str]          = None
    isActive:      Optional[bool]         = None
    openingHours:  Optional[OpeningHours] = None
