## Project Overview

This is a Python backend project built with the [FastAPI](https://fastapi.tiangolo.com/) framework. It's a lightweight and modern web framework for building APIs with Python 3.7+ based on standard Python type hints.

The project is structured as follows:

-   `main.py`: The main application file containing the FastAPI app instance and API endpoints.
-   `requirements.txt`: The file listing the project's Python dependencies.
-   `venv/`: The directory containing the Python virtual environment for this project.

## Building and Running

To get started with this project, follow these steps:

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the development server:**
    ```bash
    uvicorn main:app --reload
    ```
    The `--reload` flag makes the server restart after code changes.

The application will be running at `http://127.0.0.1:8000`.

## Development Conventions

-   **Dependencies:** All Python dependencies should be added to the `requirements.txt` file.
-   **Code Style:** While no specific linter is configured, it's recommended to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
-   **Virtual Environment:** It is recommended to use the `venv` virtual environment for development. To activate it, run:
    ```bash
    source venv/bin/activate
    ```
