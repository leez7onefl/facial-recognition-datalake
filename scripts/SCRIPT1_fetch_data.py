import os
import uuid
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../red-freedom-426709-a7-6904e9a53b27.json'
storage_client = storage.Client()
bucket_name = 'datalakes-ing3'

from datetime import datetime

def upload_images_from_folder(folder_path):

    uuids = []

    if folder_path and os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            img_path = os.path.join(folder_path, filename)
            unique_id = str(uuid.uuid4())
            uuids.append(unique_id)

            bucket = storage_client.bucket(bucket_name)
            destination_blob_name = f'0_raw/{unique_id}'
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(img_path)
            print(f"File {img_path} uploaded to {destination_blob_name}.")

    logs_file = f"../logs/{datetime.today().date()}__added_UUIDs.txt"
    with open(logs_file, 'w') as file:
        for unique_id in uuids:
            file.write(f"{unique_id}\n")

    return uuids