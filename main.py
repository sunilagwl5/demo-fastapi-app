import os
import json
import redis
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import google.auth
from google.auth.transport.requests import Request
import traceback

app = FastAPI(
    title="Demo FastAPI App",
    description="API documentation (Swagger UI) for the demo FastAPI service. Includes cache test.",
    version="1.1.2",
    docs_url="/docs",
    redoc_url="/redoc"
)

if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# -- Redis Configuration --
REDIS_HOST = os.environ.get("REDIS_HOST", "10.128.0.100")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

def get_redis_client():
    try:
        print(f"Initializing Redis (non-cluster) client for {REDIS_HOST}:{REDIS_PORT}")
        # Fetch IAM token for authentication
        credentials, project = google.auth.default(
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        credentials.refresh(Request())
        token = credentials.token
        print("Successfully retrieved IAM token")
        
        # Using standard Redis client (Valkey compatible)
        client = redis.Redis(
            host=REDIS_HOST, 
            port=REDIS_PORT, 
            password=token,
            decode_responses=True,
            ssl=False
        )
        # Force a connection test
        print("Testing connection with PING...")
        if client.ping():
            print("PONG!")
            return client
        else:
            print("PING failed")
            return None
    except Exception as e:
        print(f"Failed to create Redis client: {e}")
        traceback.print_exc()
        return None

# -- Models --
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/api")
async def read_root():
    return {"message": "Hello Perfectus Redis"}

# -- Cache Endpoints --

@app.get("/cache/test")
async def test_cache():
    client = get_redis_client()
    if not client:
        raise HTTPException(status_code=500, detail="Could not initialize Redis client. Check logs for traceback.")
    
    try:
        client.set("test_key", "Hello from Memorystore Valkey!", ex=60)
        val = client.get("test_key")
        return {"status": "success", "value": val}
    except Exception as e:
        print(f"Cache operation failed: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Cache error: {str(e)}")

# -- Item Endpoints --

@app.get("/items", response_model=List[Item])
async def get_items():
    client = get_redis_client()
    if not client:
        raise HTTPException(status_code=500, detail="Redis unavailable")
    
    try:
        raw_items = client.hvals("items")
        return [Item(**json.loads(i)) for i in raw_items]
    except Exception as e:
        print(f"Failed to fetch items: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    client = get_redis_client()
    if not client:
        raise HTTPException(status_code=500, detail="Redis unavailable")

    try:
        new_id = client.incr("item:id_counter")
        item.id = new_id
        client.hset("items", new_id, item.json())
        return item
    except Exception as e:
        print(f"Failed to create item: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    client = get_redis_client()
    if not client:
        raise HTTPException(status_code=500, detail="Redis unavailable")

    try:
        client.hdel("items", item_id)
        return {"status": "deleted", "id": item_id}
    except Exception as e:
        print(f"Failed to delete item: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint for loadbalancer
@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="::", port=port)