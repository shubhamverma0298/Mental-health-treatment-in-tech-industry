import pandas as pd
import os
from pymongo import MongoClient
from src.data.preprocess import upload_dataframe_to_mongodb
from src.models.train import train_and_save_model

def helper():
    try:
        mongo_uri = "mongodb+srv://vermabhanu0298:zXpDXRYwvUaAQlfJ@assignmentcluster.yykwoef.mongodb.net/"
        db_name = "MiniHackathonDB"
        collection_name = "ProcessedData"
        model_path = r'C:\Users\HP\PW skills\SELF placed\Machine Learning\projects\Mini Hackathon!\models\trained_model.pkl'

        # --- Check if data already exists in MongoDB ---
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        if collection.count_documents({}) > 0:
            print(f"Collection '{collection_name}' already contains data. Skipping upload.")
        else:
            print(f"Collection '{collection_name}' is empty. Uploading data from local CSV...")
            # Load data from local CSV
            df = pd.read_csv(r'C:\Users\HP\PW skills\SELF placed\Machine Learning\projects\Mini Hackathon!\data\processed\processed_data.csv')
            # Upload to MongoDB
            upload_dataframe_to_mongodb(df, mongo_uri, db_name, collection_name)
        
        client.close() # Close the initial client connection

        # --- Train and save the model ---
        # --- Check if the model file already exists ---
        if os.path.exists(model_path):
            print(f"Model file already found at {model_path}. Skipping training.")
            return # Exit the function early if the model is already there

        # --- If model does not exist, proceed with the original logic ---
        print("Model file not found. Starting data upload and training process...")
        train_and_save_model(mongo_uri, db_name, collection_name, model_path)
            
    except Exception as e:
        print(f"An error occurred in helper function: {e}")
            
# python -m src.utils.helpers
