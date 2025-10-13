import pandas as pd
from pymongo import MongoClient

def upload_dataframe_to_mongodb(df, mongo_uri, db_name, collection_name):
    """
    Connects to MongoDB and uploads a pandas DataFrame to a specified collection.

    Args:
        df: pandas DataFrame to upload.
        mongo_uri: MongoDB connection string (e.g., "mongodb://localhost:27017/").
        db_name: Name of the database.
        collection_name: Name of the collection.
    """
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # Convert DataFrame to a list of dictionaries
        data_to_insert = df.to_dict('records')

        if data_to_insert:
            collection.insert_many(data_to_insert)
            print(f"Successfully inserted {len(data_to_insert)} documents into the '{collection_name}' collection.")
        else:
            print("No data to insert from the DataFrame.")

        client.close()
        print("MongoDB connection closed.")

    except Exception as e:
        print(f"An error occurred: {e}")
        
        
def export_collection_to_dataframe(mongo_uri, db_name, collection_name):
    """
    Connects to MongoDB, retrieves data from a collection, and loads it into a pandas DataFrame.

    Args:
        mongo_uri: MongoDB connection string (e.g., "mongodb://localhost:27017/").
        db_name: Name of the database.
        collection_name: Name of the collection.

    Returns:
        pandas DataFrame containing the data from the collection, or None if an error occurs.
    """
    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # Find all documents in the collection and convert to a list
        data = list(collection.find())

        # Convert the list of dictionaries to a pandas DataFrame
        if data:
            df = pd.DataFrame(data)
            # Remove the default MongoDB '_id' column if it exists and is not needed
            if '_id' in df.columns:
                df = df.drop(columns=['_id'])
            print(f"Successfully loaded {len(data)} documents into a DataFrame.")
            return df
        else:
            print(f"No documents found in the '{collection_name}' collection.")
            return pd.DataFrame() # Return an empty DataFrame if no data

        client.close()
        print("MongoDB connection closed.")

    except Exception as e:
        print(f"An error occurred: {e}")

