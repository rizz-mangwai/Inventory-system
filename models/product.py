
def new_product(product_id, name, category_id, supplier_id, price,
                 purchase_price, quantity, reorder_level, description=""):
    return {
        "product_id": product_id,
        "name": name,
        "category_id": category_id,
        "supplier_id": supplier_id,
        "price": price,
        "purchase_price": purchase_price,
        "quantity": quantity,
        "reorder_level": reorder_level,
        "description": description
    }
