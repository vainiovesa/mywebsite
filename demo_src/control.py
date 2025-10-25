from datetime import datetime
from demo_src.fetch import get_price_now

YELLOW_BOUNDARY = 5 # Cents (Euro)
RED_BOUNDARY = 15   # Cents (Euro)

def get_info():
    current_time = datetime.now()
    price = get_price_now(current_time)
    price /= 10 # Default is tens of cents for some reason

    red = price > RED_BOUNDARY
    yellow = price > YELLOW_BOUNDARY and not red
    green = not red and not yellow

    light_control = {"r": red, "y": yellow, "g": green}

    current_time = current_time.strftime("%H:%M, %d.%m.%Y")
    price = round(price, 2)
    return current_time, price, light_control
