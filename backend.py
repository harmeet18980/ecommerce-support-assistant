
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import time

app = FastAPI(title="E-Commerce Customer Support Agent")

# Sample Data (Day-14 मधल्या values इथे टाक)
orders = {
    "1001": "Shipped",
    "1002": "Delivered",
    "1003": "Processing"
}

return_policy = """
Products can be returned within 7 days of delivery.
Refunds are processed within 5-7 business days.
"""

product_faqs = {
    "laptop": "Laptop comes with 1 year warranty.",
    "mobile": "Mobile comes with 6 months warranty.",
    "headphones": "Headphones support Bluetooth 5.0."
}

def escalate_to_human():
    return "Your query has been escalated to a human support representative."

def is_angry(text):
    angry_words = ["angry", "worst", "bad service", "frustrated"]
    return any(word in text for word in angry_words)

def translate_to_english(text):
    return text

def ecommerce_support_bot(user_input):

    translated_input = translate_to_english(user_input)
    text = translated_input.lower()

    if is_angry(text):
        return escalate_to_human()

    if "order" in text:
        words = text.split()

        for word in words:
            if word in orders:
                return f"Order {word} status: {orders[word]}"

        return "Please provide a valid order ID."

    if "return" in text or "refund" in text:
        return return_policy

    for product in product_faqs:
        if product in text:
            return product_faqs[product]

    return "Sorry, I can help with order tracking, returns, refunds, and product FAQs."

class UserQuery(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Customer Support Agent Running"}

@app.post("/chat")
def chat(query: UserQuery):
    return {
        "response": ecommerce_support_bot(query.message)
    }

@app.post("/stream")
def stream_chat(query: UserQuery):

    response_text = ecommerce_support_bot(query.message)

    def generate():
        for word in response_text.split():
            yield word + " "
            time.sleep(0.1)

    return StreamingResponse(generate(), media_type="text/plain")
