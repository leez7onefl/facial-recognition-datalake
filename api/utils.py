from google.cloud import storage
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import find_dotenv, load_dotenv
from PIL import Image
import io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../red-freedom-426709-a7-6904e9a53b27.json'

dotenv_path = find_dotenv("../keys.env", raise_error_if_not_found=True, usecwd=True)
load_dotenv(dotenv_path, override=True)

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index_name = "datalakes-ing3-curated"
index = pc.Index(index_name)

def get_raw_data(uuids=None):
    client = storage.Client()
    bucket = client.get_bucket('datalakes-ing3')
    
    if uuids is None:
        blobs = list(bucket.list_blobs(prefix='0_raw/'))
    else:
        if isinstance(uuids, str):
            uuids = [uuids]
        blobs = [bucket.blob(f'0_raw/{uuid}') for uuid in uuids]
    
    data = {}
    for blob in blobs:
        try:
            blob_data = blob.download_as_bytes()
            image = Image.open(io.BytesIO(blob_data))
            data[blob.name] = image
        except Exception as e:
            data[blob.name] = f'Error: {str(e)}'

    return data

def get_staging_data(uuids=None):
    client = storage.Client()
    bucket = client.get_bucket('datalakes-ing3')
    
    if uuids is None:
        blobs = list(bucket.list_blobs(prefix='1_staging/'))
    else:
        if isinstance(uuids, str):
            uuids = [uuids]
        blobs = [bucket.blob(f'1_staging/{uuid}') for uuid in uuids]
    
    data = {}
    for blob in blobs:
        try:
            blob_data = blob.download_as_bytes()
            image = Image.open(io.BytesIO(blob_data))
            data[blob.name] = image
        except Exception as e:
            data[blob.name] = f'Error: {str(e)}'

    return data

def get_curated_data(uuids=None):
    if uuids is None:
        return None
    if isinstance(uuids, str):
        uuids = [uuids] 

    combined_ids = ["1_staging/" + uuid for uuid in uuids]
    vector_response = index.fetch(ids=combined_ids, namespace="")
    vector = vector_response


    return vector

def check_health():
    health_info = {}
    
    try:
        client = storage.Client()
        buckets = list(client.list_buckets())
        bucket_count = len(buckets)
        gcs_status = {
            'status': 'healthy' if bucket_count > 0 else 'unreachable',
            'bucket_count': bucket_count
        }
    except Exception as e:
        gcs_status = {
            'status': 'error',
            'message': str(e)
        }
        
    health_info['google_cloud_storage'] = gcs_status

    try:
        index_status = index.describe_index_stats()
        if index_status:
            pinecone_status = {
                'status': 'healthy',
                'total_vector_count': index_status.get('total_vector_count', 0),
            }
        else:
            pinecone_status = {
                'status': 'unreachable'
            }
    except Exception as e:
        pinecone_status = {
            'status': 'error',
            'message': str(e)
        }

    health_info['pinecone'] = pinecone_status
    
    return health_info

def get_stats():
    import json
    try:
        client = storage.Client()
        
        raw_bucket = client.get_bucket('datalakes-ing3')
        raw_blobs = list(raw_bucket.list_blobs(prefix='0_raw/'))
        raw_data_count = len(raw_blobs)
        
        staging_bucket = client.get_bucket('datalakes-ing3')
        staging_blobs = list(staging_bucket.list_blobs(prefix='1_staging/'))
        staging_data_count = len(staging_blobs)
        
        index_stats = pc.describe_index(index_name)
        
        
        stats = {
            'raw_layer_data_count': raw_data_count,
            'staging_layer_data_count': staging_data_count,
            'curated_layer_pinecone_stats': f"{str(index_stats)}"
        }
        
        return stats

    except Exception as e:
        return {'error': str(e)}