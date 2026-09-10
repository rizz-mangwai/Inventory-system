
def new_sale(sale_id, product_id, customer_id, quantity, sale_price, date):
    return {
        "sale_id": sale_id,
        "product_id": product_id,
        "customer_id": customer_id,
        "quantity": quantity,
        "sale_price": sale_price,
        "date": date
    }
