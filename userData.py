import json
import os

credentials_file = "face_data/credentials.json"

# Save credentials to a JSON file
def save_credentials(security_code, password):
    credentials = {"security_code": security_code, "password": password}
    with open(credentials_file, "w") as file:
        json.dump(credentials, file)

# Load credentials from the JSON file
def load_credentials():
    if os.path.exists(credentials_file):
        with open(credentials_file, "r") as file:
            return json.load(file)
    return None
