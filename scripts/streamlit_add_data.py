import streamlit as st

from SCRIPT1_fetch_data import upload_images_from_folder
from SCRIPT2_remove_background import background_removal
from SCRIPT3_vectorize_images import vectorize_images_from_uuid

st.header("Add Faces")
file_path = st.text_input("Enter the path of your faces folder : ")

if st.button("Submit"):
    
    with st.spinner("Uploading images..."):
        uuids = upload_images_from_folder(file_path)
    st.success("Images uploaded successfully!")
    
    with st.spinner("Removing background..."):
        background_removal(uuids)
    st.success("Background removed successfully!")
    
    with st.spinner("Vectorizing images..."):
        vectorize_images_from_uuid(uuids)
    st.success("Images vectorized successfully!")