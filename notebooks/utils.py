def format_price(price):
    """Format price in Nigerian Naira with proper comma separation"""
    if price >= 1_000_000_000:
        return f"₦{price/1_000_000_000:.1f}B"
    elif price >= 1_000_000:
        return f"₦{price/1_000_000:.1f}M"
    elif price >= 1_000:
        return f"₦{price/1_000:.0f}K"
    else:
        return f"₦{price:,.0f}"

def calculate_price_per_sqm(price, size):
    """Calculate price per square meter"""
    if size > 0:
        return price / size
    return 0

def get_affordability_category(price):
    """Categorize property by affordability"""
    if price < 30_000_000:
        return "Budget-Friendly"
    elif price < 80_000_000:
        return "Mid-Range"
    elif price < 150_000_000:
        return "Premium"
    else:
        return "Luxury"