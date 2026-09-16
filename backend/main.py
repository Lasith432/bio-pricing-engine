from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Bio-Pricing Engine API")

# 1. Pydantic Model (මෙහි ඇත්තේ inputs පමණි)
class SensorInput(BaseModel):
    product_name: str
    base_price: float
    current_temp: float
    humidity: float

# 2. සාමාන්‍ය Python Function
def calculate_shelf_life(temp: float, humidity: float) -> float:
    decay_factor = (temp - 15.0) * 2.5
    remaining_hours = 48.0 - decay_factor
    return max(2.0, remaining_hours)

# 3. GET Endpoint (items ලැයිස්තුව තිබිය යුත්තේ මෙතැනයි)
@app.get("/api/products")
def get_products():
    items = [
        {"id": 1, "name": "Fresh Tomatoes", "base_price": 400.0},
        {"id": 2, "name": "Local Carrots", "base_price": 350.0}
    ]
    return {"status": "success", "count": len(items), "data": items}

# 4. POST Endpoint
@app.post("/api/predict-price")
def predict_price(payload: SensorInput):
    rsl = calculate_shelf_life(payload.current_temp, payload.humidity)

    discount_rate = 0
    if rsl < 12.0:
        discount_rate = 50
    elif rsl < 24.0:
        discount_rate = 25

    final_price = payload.base_price * (1 - (discount_rate / 100))

    return {
        "product": payload.product_name,
        "storage_temperature": payload.current_temp,
        "remaining_shelf_life_hours": round(rsl, 1),
        "applied_discount_percent": discount_rate,
        "original_price": payload.base_price,
        "dynamic_price": round(final_price, 2)
    }