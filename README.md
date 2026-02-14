# Demo FastAPI App

This is a simple FastAPI application that manages a list of items and provides a welcome message.

## API Endpoints

- `GET /`: Serves the frontend application.
- `GET /api`: Returns a welcome message: `{"message": "Hello vibedoctor !"}`.
- `GET /items`: Returns a list of items.
- `POST /items`: Adds a new item.
- `DELETE /items/{item_id}`: Deletes an item.
- `GET /health`: Health check endpoint.

## Running the App

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

## Running Tests

To run the tests, execute:
```bash
pytest
```