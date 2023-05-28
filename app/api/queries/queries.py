from sqlalchemy import extract, func
from api.models.models import Customer, Product, SalesReceipt


def birthday_customers_query(db, date):
    """Birthday customers query."""
    # Retrieve customers whose birthdate matches the current month and day
    customers = (
        db.query(Customer)
        .filter(
            func.date_part("month", Customer.birthdate) == date.month,
            func.date_part("day", Customer.birthdate) == date.day,
        )
        .all()
    )

    return [
        {
            "customer_id": customer.customer_id,
            "customer_first_name": customer.customer_first_name,
        }
        for customer in customers
    ]


def top_selling_products_query(year, db, limit=10):
    """Top-selling products query for a specific year."""

    # Subquery to calculate the total sales for each product
    sales_subquery = (
        db.query(
            SalesReceipt.product_id,  # Select the product_id
            func.sum(SalesReceipt.quantity).label("total_sales")
            # Calculate the sum of quantity and label it as total_sales
        )
        .filter(extract("year", SalesReceipt.transaction_date) == year)
        .group_by(SalesReceipt.product_id)
        .order_by(func.sum(SalesReceipt.quantity).desc())
        .limit(limit)
        .subquery()
    )

    # Join the subquery with the Product table to get product details
    products_query = (
        db.query(
            Product.product,  # Select the product name
            sales_subquery.c.total_sales.label("total_sales")
            # Select the total sales from the subquery and label it as total_sales
        )
        .join(sales_subquery, Product.product_id == sales_subquery.c.product_id)
        .all()  # Retrieve all the results
    )

    return [
        {"product_name": product, "total_sales": total_sales}
        for product, total_sales in products_query
    ]


def last_order_per_customer_query(db):
    """Last order per customer query."""

    # Subquery to retrieve the last order date for each customer
    subquery = (
        db.query(
            SalesReceipt.customer_id,
            func.max(SalesReceipt.transaction_date).label("last_order_date"),
        )
        .group_by(SalesReceipt.customer_id)
        .subquery()
    )

    # Join the subquery with the Customer table to get customer details
    result = (
        db.query(
            Customer.customer_id, Customer.customer_email, subquery.c.last_order_date
        )
        .join(subquery, Customer.customer_id == subquery.c.customer_id)
        .all()
    )

    # Prepare the response dictionary
    response = {"customers": []}
    for customer_id, customer_email, last_order_date in result:
        # Append each customer's details to the response
        response["customers"].append(
            {
                "customer_id": customer_id,
                "customer_email": customer_email,
                "last_order_date": last_order_date,
            }
        )

    return [
        {
            "customer_id": customer_id,
            "customer_email": customer_email,
            "last_order_date": last_order_date,
        }
        for customer_id, customer_email, last_order_date in result
    ]
