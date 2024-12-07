def determine_delivery_system(customer_city, store_city):
    """
    Determines the delivery system based on the customer's and store's city.

    Args:
        customer_city (str): The city where the customer lives.
        store_city (str): The city where the store is located.

    Returns:
        str: "Delivery System 1" or "Delivery System 2"
    """
    if customer_city.lower() == "sari" and store_city.lower() == "sari":
        return "Delivery System 1"
    else:
        return "Delivery System 2"
