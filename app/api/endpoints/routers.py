from fastapi import APIRouter, Depends
from datetime import date
from sqlalchemy.orm import Session
from core.database import SessionLocal
from api.queries.queries import (
    birthday_customers_query,
    top_selling_products_query,
    last_order_per_customer_query,
)


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/customers/birthday")
def get_birthday_customers(session: Session = Depends(get_db)):
    """Get endpoint for today's birthday customers"""
    today = date.today()
    return {"customers": birthday_customers_query(session, today)}


@router.get("/products/top-selling-products/{year}")
def get_top_ten_selling_products(year: int, session: Session = Depends(get_db)):
    """Get endpoint for 10 top-selling products for a given 'year'"""
    return {"products": top_selling_products_query(year, session, limit=10)}


@router.get("/customers/last-order-per-customer")
def get_last_order_per_customer(session: Session = Depends(get_db)):
    """Get endpoint for last order of every customer"""
    return {"customers": last_order_per_customer_query(session)}
