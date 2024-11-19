import json
import socket
from fastapi import FastAPI
from contextlib import asynccontextmanager

SCRAPER_HOST = "127.0.0.1"
SCRAPER_PORT = 65432

async def activate_scraper():
    """Activate the scraper by sending a payload to the scraper service."""
    try:
        activation_status = "True"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(10)  # Set a timeout for the connection
            client_socket.connect((SCRAPER_HOST, SCRAPER_PORT))

            payload = {"activation_status": activation_status}
            client_socket.sendall(json.dumps(payload).encode())

            try:
                response = client_socket.recv(1024).decode()
                print(f"Activation response: {response}")
            except socket.timeout:
                print("No response received from the scraper within the timeout.")
    except Exception as e:
        print(f"Error during activation: {str(e)}")

# Using AsyncContextManager from contextlib to manage lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler for startup and shutdown tasks using AsyncContextManager."""
    print("Application starting up...")
    await activate_scraper()  # Activate the scraper during startup

    # Yield to indicate that the application is now running
    yield

    print("Application shutting down...")  # Perform any cleanup tasks here

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"Status": "API is running and scraper activated on startup"}
