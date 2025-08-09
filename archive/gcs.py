from dotenv import load_dotenv
import os
from google.cloud import storage

load_dotenv()  # Load environment variables from .env

def upload_json_to_meals_bucket(local_json_path, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket("meals-bucket")
    blob = bucket.blob(destination_blob_name)

    with open(local_json_path, "r") as f:
        json_data = f.read()

    blob.upload_from_string(json_data, content_type="application/json")
    print(f"Uploaded {local_json_path} to gs://meals-bucket/{destination_blob_name}")

if __name__ == "__main__":
    local_json_path = "meals-pro.json"  # Your local JSON file path
    destination_blob_name = "uploaded-file.json"  # Target filename in GCS

    upload_json_to_meals_bucket(local_json_path, destination_blob_name)
