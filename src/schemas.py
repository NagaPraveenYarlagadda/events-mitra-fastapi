# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: int
    currency: str
    info: str
    short_description: str
    full_description: str
    

class Product(ProductBase):
    slug: str
    class Config:
        orm_mode = True
class FunctionHall(BaseModel):
    id: int
    name: str
    capacity: int
    location: str
    contact_person: str
    contact_number: str

class FunctionHallCreate(BaseModel):
    name: str
    capacity: int
    location: str
    contact_person: str
    contact_number: str

class BookingCreate(BaseModel):
    hall_name: str
    date: str
    start_time: str
    end_time: str
    customer_name: str

class Booking(BaseModel):
    booking_id: int
    hall_name: str
    date: str
    start_time: str
    end_time: str
    customer_name: str
    booking_status: str