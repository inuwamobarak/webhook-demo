from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# In-memory database to store orders
orders = []

# Registered webhook URLs
webhooks = []

class Order(BaseModel):
    id: int
    product_name: str
    quantity: int
    price: float

class WebhookURL(BaseModel):
    url: str

@app.post("/orders/")
def create_order(order: Order):
    orders.append(order)
    # Notify registered webhooks
    notify_webhooks(order)
    return {"message": "Order created successfully!", "order": order}

@app.get("/orders/")
def list_orders():
    return orders

@app.post("/webhooks/")
def register_webhook(webhook: WebhookURL):
    if webhook.url in webhooks:
        raise HTTPException(status_code=400, detail="Webhook URL already registered.")
    webhooks.append(webhook.url)
    return {"message": "Webhook registered successfully!", "webhook": webhook}

@app.get("/webhooks/")
def list_webhooks():
    return {"webhooks": webhooks}

def notify_webhooks(order: Order):
    for webhook in webhooks:
        try:
            response = requests.post(webhook, json=order.dict(), timeout=5)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to notify webhook {webhook}: {e}")