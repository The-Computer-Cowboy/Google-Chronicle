# Import libraries
import requests
import subprocess

# Define API endpoint and list information
API_URL = "https://backstory.googleapis.com/v2/lists"
LIST_NAME = "list_name"
UPDATE_MASK = "list.description,list.lines"

# Download the blackbook.txt file (replace with your preferred location)
BLACKBOOK_FILE = "blackbook.txt"
download_command = f"curl -sSL https://raw.githubusercontent.com/stamparm/blackbook/master/blackbook.txt > {BLACKBOOK_FILE}"
subprocess.run(download_command.split(), check=True)  # Run curl command

# Read downloaded file content
try:
    with open(BLACKBOOK_FILE, "r") as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"Error: Could not find downloaded file {BLACKBOOK_FILE}")
    exit(1)

# Prepare list data
LIST_DATA = {
    "name": LIST_NAME,
    "description": "List from blackbook.txt",
    "lines": lines,  # Use downloaded lines
    "content_type": "TEXT",  # Update content type if needed
}

# Headers with appropriate content type
headers = {"Content-Type": "application/json"}

# Update the list using PATCH request
try:
    response = requests.patch(
        f"{API_URL}?update_mask={UPDATE_MASK}", headers=headers, json=LIST_DATA
    )
    response.raise_for_status()  # Raise exception for non-2xx status codes
    print("List updated successfully!")
except requests.exceptions.RequestException as e:
    print(f"Error updating list: {e}")

# Clean up downloaded file (optional)
# subprocess.run(["rm", BLACKBOOK_FILE])
