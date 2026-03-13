import os
import json
import redis
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Demo FastAPI App",
    description="API documentation (Swagger UI) for the demo FastAPI service. Includes root and health endpoints.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# -- Models --
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

# -- Redis Connection --
def get_redis_client():
    redis_url = os.environ.get("REDIS_URL")
    if redis_url:
        return redis.from_url(redis_url, decode_responses=True)
    host = os.environ.get("REDISHOST", "localhost")
    port = int(os.environ.get("REDISPORT", 6379))
    user = os.environ.get("REDISUSER", None)
    password = os.environ.get("REDISPASSWORD", None)
    return redis.Redis(host=host, port=port, username=user, password=password, decode_responses=True)

redis_client = get_redis_client()

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/api")
async def read_root():
    return {"message": "Hello, FastAPI!"}

# -- Item Endpoints --

@app.get("/items", response_model=List[Item])
async def get_items():
    return items

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    global current_id
    current_id += 1
    item.id = current_id
    items.append(item)
    return item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    global items
    items = [item for item in items if item.id != item_id]
    return {"status": "deleted", "id": item_id}

# Health check endpoint for loadbalancer
@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="::", port=port)
