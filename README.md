# webhook-demo

You need about 4 terminals open to use the webhook:
1. Start the normal FastAPI server: ``uvicorn main:app --reload --port 8000``
2. Start the webhook server: `` uvicorn webhook_handler:app --reload --port 8001``
3. Register a URL for webhook: `` curl -X POST "http://127.0.0.1:8000/webhooks/" -H "Content-Type: application/json" -d '{"url": "http://127.0.0.1:8001/webhook-receiver/"}'``
4. Test Webhook: ``curl -X POST "http://127.0.0.1:8000/orders/" -H "Content-Type: application/json" -d '{"id": 1, "product_name": "Laptop", "quantity": 2, "price": 1500.00}'``

To use the celery and redis scheduler:
If on Mac, use brew to install redis:
* Install Redis:
``brew install redis``

Start Redis:
``brew services start redis``

Start celery worker: `` celery -A tasks worker --loglevel=info``
Start celery beat: ``celery -A tasks beat --loglevel=info``