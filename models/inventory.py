

def new_inventory_record(inventory_id, product_id, quantity_in_stock, last_updated):
    return {
        "inventory_id": inventory_id,
        "product_id": product_id,
        "quantity_in_stock": quantity_in_stock,
        "last_updated": last_updated
    }
