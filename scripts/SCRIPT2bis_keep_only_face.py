from google.cloud import storage
from rembg import new_session, remove
from pathlib import Path
from PIL import Image
import io
import os
import face_recognition

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../red-freedom-426709-a7-6904e9a53b27.json'
storage_client = storage.Client()
bucket_name = 'datalakes-ing3'

session = new_session()
bucket = storage_client.bucket(bucket_name)

input_dir = '0_raw/'
output_dir = '1_staging/'

def background_removal(uuid_list):
    blobs = storage_client.list_blobs(bucket_name, prefix=input_dir)

    for blob in blobs:
        if Path(blob.name).stem in uuid_list:
            input_content = blob.download_as_bytes()
            
            output_content = face_recognition.face_locations(input_content)
            top, right, bottom, left = output_content
            face_image = input_content[top:bottom, left:right]
            output_image = Image.fromarray(face_image)
            
            if output_image.mode == 'RGBA':
                output_image = output_image.convert('RGB')
            
            output_image = output_image.resize((224, 224), Image.LANCZOS)
            
            output_buffer = io.BytesIO()
            output_image.save(output_buffer, format='JPEG')
            output_buffer.seek(0)
            
            filename = Path(blob.name).stem + '.nbg.jpg'
            output_blob_name = f'{output_dir}{filename}'

            output_blob = bucket.blob(output_blob_name)
            output_blob.upload_from_file(output_buffer, content_type='image/jpeg')