from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook-receiver/")
async def webhook_receiver(request: Request):
    payload = await request.json()
    print(f"Webhook received: {payload}")
    return {"message": "Webhook received successfully!"}