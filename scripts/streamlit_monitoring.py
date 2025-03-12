import streamlit as st
import requests
from PIL import Image
from io import BytesIO

BASE_URL = "http://localhost:5000"

def get_image_data(type, uuid):
    response = requests.get(f"{BASE_URL}/{type}?uuid={uuid}")
    return response

def get_pinecone_data(uuid):
    response = requests.get(f"{BASE_URL}/curated?uuid={uuid}")
    return response

def check_health():
    response = requests.get(f"{BASE_URL}/health")
    return response

def get_stats():
    response = requests.get(f"{BASE_URL}/stats")
    return response

st.header("Monitoring Panel")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Health Check")
    health_response = check_health()
    if health_response.status_code == 200:
        st.write(health_response.json())
    else:
        st.error("Failed to get health status")

with col2:
    st.subheader("API Stats")
    stats_response = get_stats()
    if stats_response.status_code == 200:
        st.write(stats_response.json())
    else:
        st.error("Failed to get stats")

uuid = st.text_input("Enter UUID:", value="7d931715-1ef9-40a4-abbf-b1cab72b3453")

if st.button("Get All Data Layers"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Raw Data")
        response = get_image_data("raw", uuid + ".jpg")
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption='Raw Data Image', use_container_width=True)
        else:
            st.error("Failed to get raw data")

    with col2:
        st.subheader("Staging Data")
        response = get_image_data("staging", uuid + ".out.jpg")
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption='Staging Data Image', use_container_width=True)
        else:
            st.error("Failed to get staging data")

    with col3:
        st.subheader("Curated Data")
        response = get_pinecone_data(uuid + ".out.jpg")
        st.write(str(response.content))
