import requests
import uvicorn
import threading
import time
import pytest

from main import app

def run_uvicorn():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

@pytest.fixture(scope="module")
def server():
    # Start the server in a separate thread
    thread = threading.Thread(target=run_uvicorn)
    thread.daemon = True
    thread.start()
    
    # Wait for the server to start
    timeout = 30
    start_time = time.time()
    while True:
        try:
            response = requests.get("http://127.0.0.1:8000")
            if response.status_code == 200:
                print("Server started successfully.")
                break
        except requests.exceptions.ConnectionError:
            pass
        if time.time() - start_time > timeout:
            raise RuntimeError("Server did not start within the given timeout.")
        time.sleep(0.5)
    
    yield
    # No explicit shutdown needed as the thread is a daemon and will exit with the main program

def test_read_root(server):
    response = requests.get("http://127.0.0.1:8000")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}

