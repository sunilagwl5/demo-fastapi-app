from fastapi import FastAPI

app = FastAPI(
    title="Demo FastAPI App",
    description="API documentation (Swagger UI) for the demo FastAPI service. Includes root and health endpoints.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}


# Health check endpoint for loadbalancer
@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
