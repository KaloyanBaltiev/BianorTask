from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from core.database import Base


class Customer(Base):
    __tablename__ = "customer"

    customer_id: int = Column(Integer, primary_key=True, index=True)
    home_store: int = Column(Integer)
    customer_first_name: str = Column("customer_first-name", String)
    customer_email: str = Column(String)
    customer_since: str = Column(String)
    loyalty_card_number: str = Column(String)
    birthdate: Date = Column(Date)
    gender: str = Column(String)
    birth_year: int = Column(Integer)


class Product(Base):
    __tablename__ = "product"

    product_id: int = Column(Integer, primary_key=True, index=True)
    product_group: str = Column(String)
    product_category: str = Column(String)
    product_type: str = Column(String)
    product: str = Column(String)
    product_description: str = Column(String)
    unit_of_measure: str = Column(String)
    current_wholesale_price: float = Column(Float)
    current_retail_price: str = Column(String)
    tax_exempt_yn: str = Column(String)
    promo_yn: str = Column(String)
    new_product_yn: str = Column(String)


class SalesReceipt(Base):
    __tablename__ = "sales_receipts"

    transaction_id: int = Column(Integer, primary_key=True, index=True)
    transaction_date: str = Column(String)
    transaction_time: str = Column(String)
    sales_outlet_id: int = Column(Integer)
    staff_id: int = Column(Integer)
    customer_id: int = Column(Integer, ForeignKey("customer.customer_id"))
    instore_yn: str = Column(String)
    order: int = Column(Integer)
    line_item_id: int = Column(Integer)
    product_id: int = Column(Integer, ForeignKey("product.product_id"))
    quantity: int = Column(Integer)
    line_item_amount: float = Column(Float)
    unit_price: float = Column(Float)
    promo_item_yn: str = Column(String)
