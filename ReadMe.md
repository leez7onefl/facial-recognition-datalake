---

# Projet Final Data Lakes

This repository contains the final project for the Data Lakes & Data Integration course at EFREI, 2025.

## Project Overview

The objective of this project is to design and implement a complete data lake solution, from data ingestion to API exposure. [The base dataset](https://www.kaggle.com/datasets/vishesh1412/celebrity-face-image-dataset) is constitued of 1800 pictures of pictures of eighteen different celebrities. 

The datalake have three layer : "raw", "staging" and "curated". 
- The raw layer contains all images, stored in a Google Blob Storage Bucket. 
- The staging layer have the same architectures, but contains only faces cut out from pictures of the raw layer, in 224*224 pixels, jpg format.

  ![image](https://github.com/user-attachments/assets/a71dae57-3b34-42ee-8eb6-046a40d3b728)

- The last layer is the curated one, containing vectorial representation of all faces of the staging layer. The curated layer use PineCone cloud vector database.

![image](https://github.com/user-attachments/assets/b9dffbe6-fab4-4be3-8ee0-727ddd9ade33)

The first operation from raw to staging mainly use SCM-CNN(U²Net) model. It uses channel global average and max pooling for image background removal (based on this [article](https://arxiv.org/pdf/2005.09007)). Also force the image to be a .jpg and resize to 244*244 using Lanczos.

![image](https://github.com/user-attachments/assets/1e8bf5d9-67e7-4b35-b312-b3721e3339ed)

The second operation from staging to curated use a VGG16 model minus classification top layers (in order to only capture features). My output vector is of dimension 4096. I then normalize it and store it. 

![image](https://github.com/user-attachments/assets/314c530f-c9b6-469c-885b-53c1f8bf5c1a)

The ultimate goal of my pipeline is to be able to upload new pictures into the database, and be able to ingest a picture to find the best match among the database.

## Project Structure

```
PROJET_FINAL_DATALAKES/
│
├── api/
│   ├── app.py                # Main API application
│   ├── routes.py             # API endpoint routes
│   └── utils.py              # Utility functions for the API
│
├── data-to-add/
│   ├── celeb_dataset_already_added    # datasets to be added
│
├── logs/
│   └── YYYY-MM-DD_UUID           # Logs of processes
│
├── notebooks/       #all tests ran before main coding
│   └── test_1.ipynb
│   └── test_2.ipynb
│   └── test_3.ipynb
│
├── pipelines/
│   ├── airflow_dags/         # Apache Airflow DAGs
│   └── image_processing_dag.py #
│
├── scripts/
│   ├── SCRIPT1_fetch_data.py         # fill raw layer
│   ├── SCRIPT2_remove_background.py  # raw to staging
│   ├── SCRIPT3_vectorize_images.py   # staging to curated
│   └── streamlit_main.py             # Main Streamlit app 
│   └── streamlit_monitoring
│   └── streamlit_add_data            # add faces to dataset
│   └── streamlit_lookalike           # similarity search
│
├── build.bat                # Batch file for building project
├── keys.env                 # Environment variables file
├── launch_streamlit.bat     # Batch file to launch Streamlit 
├── README.md                # Project documentation file
├── red-freedom-426709-a7-6904e9a53b27.json
├── requirements.txt         # Python dependencies
```
___

## Getting Started

### Prerequisites

- Python 3.8+
- Apache Airflow
- Streamlit

___
### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/leez7onefl/facial-recognition-datalake
    ```

2. Install dependencies into a virtual environment :
    ```bash
    built.bat
    ```

3. Configure environment variables:
   - Create a `keys.env` to store your PineCone API KEY

4. Put your Google Storage JSON access credentials at root

___
### Run Streamlit App

In order to get the best experience, please prefer the use of the streamlit application. 
```bash
launch_streamlit.bat
```

#### The streamlit UI contain three pages : 

![image](https://github.com/user-attachments/assets/ff7ce53a-9bef-4158-8d13-cd9ed60aff79)

___

![image](https://github.com/user-attachments/assets/9a3bddb0-1b63-4d5d-b5c0-e78228b57a66)

___

![image](https://github.com/user-attachments/assets/7e4d3cff-e5f5-4e40-9cd9-c5d6fd158e17)

___

![image](https://github.com/user-attachments/assets/f4f26975-d43d-4793-8086-53f814fc7105)

___

![image](https://github.com/user-attachments/assets/15dae39f-7748-41df-bb9d-51ad3a09c978)

___

#### EDIT v2 : 

First version hads't accomplished the original purpose I intended to create, wich is a datalake system able to compare a face to a pre-build database. 
First version used a SCM-CNN(U²Net) model trained onto channels average, height, and width of pictures. 
Second version now use dlib pre-trained model that is composed of a linear SVM trained on histogram of gradients in pictures [(see paper)](https://www.researchgate.net/profile/Mahdi-Jampour/publication/284367679_Efficient_Handwritten_Digit_Recognition_based_on_Histogram_of_Oriented_Gradients_and_SVM/links/575d3c8608ae9a9c9559f7a6/Efficient-Handwritten-Digit-Recognition-based-on-Histogram-of-Oriented-Gradients-and-SVM.pdf) for face detection only :

![image](https://github.com/user-attachments/assets/76b52038-13ff-470c-aa03-d7d5a2040669)

![image](https://github.com/user-attachments/assets/5a17f303-ce29-412b-89a0-8a26410259a6)

![image](https://github.com/user-attachments/assets/d3e1a9a7-48eb-4925-9a25-781414f883ff)


#### New results before storing in curated layer : 

![image](https://github.com/user-attachments/assets/17ddf78c-a9db-42df-a567-8941c6cfd20c)

![image](https://github.com/user-attachments/assets/fbc2af39-88a7-47bb-b6e7-6d288d935655)

![image](https://github.com/user-attachments/assets/aa62a89f-e871-4870-8b08-3b877acd85d1)


___

#### Execute Pipelines

1. Set up and start Apache Airflow.
2. Trigger the desired DAG from the `airflow_dags` directory.

## Contribution

Feel free to contribute by creating issues or submitting pull requests.

## Contact

For any queries, please contact me at leonard.gonzalez@outlook.fr.

---
