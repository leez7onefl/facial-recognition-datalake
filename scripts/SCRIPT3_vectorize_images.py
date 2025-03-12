from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from keras.preprocessing import image

import numpy as np
from PIL import Image
import io
from pinecone import Pinecone
from google.cloud import storage
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../red-freedom-426709-a7-6904e9a53b27.json'

storage_client = storage.Client()
bucket_name = 'datalakes-ing3'


dotenv_path = find_dotenv("../keys.env", raise_error_if_not_found=True, usecwd=True)
load_dotenv(dotenv_path, override=True)

pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pinecone.Index('datalakes-ing3-curated')

def extract_features(image_bytes):
    base_model = VGG16(weights='imagenet', include_top=True)
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc2').output)
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((224, 224))
    img_data = np.expand_dims(image.img_to_array(img), axis=0)
    img_data = preprocess_input(img_data)
    
    vgg16_feature = model.predict(img_data)
    flat_feature = vgg16_feature.flatten()
    return flat_feature

def vectorize_images_from_uuid(uuid_list, bucket_name='datalakes-ing3'):

    blobs = storage_client.list_blobs(bucket_name, prefix='1_staging/', delimiter='/')

    for blob in blobs:
        file_uuid = Path(blob.name).stem.split('.')[0]
        if file_uuid in uuid_list:
            try:
                img_content = blob.download_as_bytes()
                features = extract_features(img_content)
                features /= np.linalg.norm(features)
                index.upsert([(blob.name, features)])
                print(f"Processed {blob.name}")

            except Exception as e:
                print(f"Error processing {blob.name}: {e}")