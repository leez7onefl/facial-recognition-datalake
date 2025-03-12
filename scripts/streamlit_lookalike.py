import streamlit as st
from SCRIPT3_vectorize_images import extract_features
import numpy as np
from pinecone import Pinecone
import os
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

BASE_URL = "http://localhost:5000"

def get_image_data(uuid):
    response = requests.get(f"{BASE_URL}/raw?uuid={uuid}")
    return response

pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pinecone.Index('datalakes-ing3-curated')

st.header("Who is My Lookalike?")

file_path = st.file_uploader("A superb picture of you:", accept_multiple_files=False, label_visibility="visible")

if st.button("Submit"):
    if file_path is not None:
        # Open and resize the image to 244x244
        image = Image.open(file_path)
        image = image.resize((244, 244))
        
        # Convert the resized image back to bytes
        img_bytes_io = BytesIO()
        image.save(img_bytes_io, format='JPEG')
        image_bytes = img_bytes_io.getvalue()

        features = extract_features(image_bytes)
        features /= np.linalg.norm(features)

        encodedNumpyData = features.astype(float).tolist()
        
        with st.spinner("Searching for your best match..."):            
            response = index.query(
                vector=encodedNumpyData,
                top_k=1,
                include_values=False,
                include_metadata=False,
            )
            
            if 'matches' in response:
                matches = response['matches']
                if matches:
                    data = [
                        {
                            'ID': match['id'],
                            'Score': match['score']
                        }
                        for match in matches
                    ]
                    df = pd.DataFrame(data)
                    st.write("Top Matches:")
                    st.write(df)

                    # Extract UUID from the first match ID
                    first_match_id = matches[0]['id']
                    # Remove prefix and suffix
                    uuid = first_match_id.replace('1_staging/', '').replace('.nbg.jpg', '')

                    response = get_image_data(uuid)
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        st.image(image, caption='Raw Data Image', use_container_width=True)
                    else:
                        st.error("Failed to get raw data")
                else:
                    st.write("No matches found.")
            else:
                st.write("Response does not contain 'matches'.")