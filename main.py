import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Product, Drop, Measurement, QuizResult, Order, UserProfile

app = FastAPI(title="Kinfash API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"brand": "Kinfash", "status": "ok"}

# ----- Catalog endpoints -----
@app.get("/api/products", response_model=List[Product])
def list_products(category: Optional[str] = None, tag: Optional[str] = None, limit: int = 24):
    filter_query = {}
    if category:
        filter_query["category"] = category
    if tag:
        filter_query["tags"] = {"$in": [tag]}
    docs = get_documents("product", filter_query, limit)
    # Cast _id to string and ensure response matches model
    cleaned = []
    for d in docs:
        d.pop("_id", None)
        cleaned.append(Product(**d))
    return cleaned

@app.post("/api/products", status_code=201)
def create_product(product: Product):
    try:
        _id = create_document("product", product)
        return {"id": _id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Drops
@app.get("/api/drops", response_model=List[Drop])
def list_drops(limit: int = 10):
    docs = get_documents("drop", {}, limit)
    cleaned = []
    for d in docs:
        d.pop("_id", None)
        cleaned.append(Drop(**d))
    return cleaned

@app.post("/api/drops", status_code=201)
def create_drop(drop: Drop):
    _id = create_document("drop", drop)
    return {"id": _id}

# Measurements
@app.post("/api/measurements", status_code=201)
def save_measurements(m: Measurement):
    _id = create_document("measurement", m)
    return {"id": _id}

# Style quiz
@app.post("/api/quiz", status_code=201)
def save_quiz(result: QuizResult):
    _id = create_document("quizresult", result)
    return {"id": _id}

# Orders (quick checkout)
@app.post("/api/orders", status_code=201)
def create_order(order: Order):
    _id = create_document("order", order)
    return {"id": _id, "status": "created"}

# Personalization profile
@app.post("/api/profile", status_code=201)
def save_profile(profile: UserProfile):
    _id = create_document("userprofile", profile)
    return {"id": _id}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
