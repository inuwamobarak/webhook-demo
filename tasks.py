from celery import Celery
from celery.schedules import crontab
import requests

celery_app = Celery(
    "webhook_demo",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

@celery_app.task
def create_test_order():
    payload = {
        "id": 1,
        "product_name": "Test Product",
        "quantity": 1,
        "price": 100.0,
    }
    try:
        response = requests.post(
            "http://127.0.0.1:8000/orders/",
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        print("Order Created")
        return f"Order created: {response.json()}"
    except Exception as e:
        return f"Failed to create order: {e}"

# Periodic Task Schedule
celery_app.conf.beat_schedule = {
    "create-order-every-5-minutes": {
        "task": "tasks.create_test_order",
        "schedule": crontab(minute="*/1"), # One minute
    }
}
celery_app.conf.timezone = "UTC"