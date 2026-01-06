default_currency = "USD"
tax_rate=0.21

vip_discount = 50
save10_discount = 0.10
save20_discount=0.20

vip_min = 100
save20_min=200

vip_min_discount=10



def parse_request(request: dict):
    user_id = request.get("user_id")
    items = request.get("items")
    coupon = request.get("coupon")
    currency = request.get("currency")
    return user_id, items, coupon, currency

def validate_user_data(user_id,items,currency):
    if user_id is None:
        raise ValueError("user_id is required")
    if items is None:
        raise ValueError("items is required")
    if currency is None:
        currency = default_currency
    return currency

def validate_items(items):
    if type(items) is not list:
        raise ValueError("items must be a list")
    if len(items) == 0:
        raise ValueError("items must not be empty")

    for it in items:
        if "price" not in it or "qty" not in it:
            raise ValueError("item must have price and qty")
        if it["price"] <= 0:
            raise ValueError("price must be positive")
        if it["qty"] <= 0:
            raise ValueError("qty must be positive")


def calculate_subtotal(items):
    return sum(item["price"] * item["qty"] for item in items)

def calculate_discount(coupon, subtotal):
    if coupon is None or coupon == "":
        return 0
    elif coupon == "SAVE10":
        discount = int(subtotal * 0.10)
    elif coupon == "SAVE20":
        if subtotal >= 200:
            discount = int(subtotal * 0.20)
        else:
            discount = int(subtotal * 0.05)
    elif coupon == "VIP":
        discount = 50
        if subtotal < 100:
            discount = 10
    else:
        raise ValueError("unknown coupon")
    return discount


def calculate_tax(total_after_discount):
    tax = int(total_after_discount * tax_rate)
    return tax, total_after_discount + tax

def generate_order_id(user_id, items_count):
    return f"{user_id}-{items_count}-X"

def process_checkout(request: dict) -> dict:
    user_id, items, coupon, currency = parse_request(request)

    currency = validate_user_data(user_id, items, currency)
    validate_items(items)

    subtotal = calculate_subtotal(items)

    discount = calculate_discount(coupon, subtotal)

    total_after_discount = max(0, subtotal - discount)
    tax, total = calculate_tax(total_after_discount)

    order_id = generate_order_id(user_id, len(items))

    return {
        "order_id": order_id,
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }
