import json
import time
import socket
from bs4 import BeautifulSoup

# Load the URL database
with open("url_database.json", "r") as f:
    url_database = json.load(f)

def data_scraper(file_path, selectors, media_type):
    """Scrape media data from a local HTML file."""
    try:
        print(f"Scraping file: {file_path}")  # Log file scraping progress
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")  # Parse the file with BeautifulSoup

        media_list = []
        # Loop through each movie item based on the CSS selectors
        for item in soup.select(selectors["item"]):
            title = item.select_one(selectors["title"]).text.strip()  # Extract movie title
            year = item.select_one(selectors["year"]).text.strip("()")  # Extract year (remove parentheses)
            poster = item.select_one(selectors["poster"])["src"]  # Extract poster image URL

            media_list.append({"type": media_type, "title": title, "year": year, "poster": poster})
        return media_list
    except Exception as e:
        print(f"Error scraping {file_path}: {str(e)}")
        return []

def unique_data_check(scraped_data):
    """Stub function to check for unique data."""
    return scraped_data  # You can implement deduplication logic here.

def save_data(data):
    """Save scraped data to a file."""
    with open("scraped_data.json", "w") as f:
        json.dump(data, f, indent=4)

def connection_handler(client_socket):
    try:
        request_data = client_socket.recv(1024).decode()  # Receive activation data
        data = json.loads(request_data)

        activation_status = data.get("activation_status")
        if activation_status == "True":
            print("Activation successful, starting scraping.")
            # Loop through the URL database
            for url, config in url_database.items():

                # Scrape the data from the local file using the defined selectors
                scraped_data = data_scraper(url, config["selectors"], config["type"])
                # Perform any unique data checks (if needed)
                unique_data = unique_data_check(scraped_data)
                # Save the scraped data to a file
                save_data(unique_data)

            print("Scraping has been completed. Waiting 24 hours before next scraping.")
            # Send a message back to the API that the scraping process is complete
            response = {"status": "scraping_complete"}
            client_socket.sendall(json.dumps(response).encode())  # Send response back
            time.sleep(86400)  # Wait for 24 hours before the next scrape
        else:
            print("Activation status is not True, scraping skipped.")
    except Exception as e:
        print(f"Error: {str(e)}")
        client_socket.sendall(json.dumps({"error": str(e)}).encode())
    finally:
        client_socket.close()

def start_scraper():
    HOST = "127.0.0.1"
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        
        print(f"Server is listening on port: {PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Client connected from {addr}")
            connection_handler(client_socket)

if __name__ == "__main__":
    start_scraper()
