import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
from src.data.preprocess import export_collection_to_dataframe

def train_and_save_model(mongo_uri, db_name, collection_name, model_path):
    """
    Connects to MongoDB, retrieves data from a specified collection, trains a CatBoost model,
    and saves the trained model to a file.

    Args:
        mongo_uri: MongoDB connection string (e.g., "mongodb://localhost:27017/")or to your mongodb site .
        db_name: Name of the database.
        collection_name: Name of the collection.
        model_path: Path to save the trained model (e.g., "catboost_model.pkl").
    """
    try:
        # Export data from MongoDB to a pandas DataFrame
        df = export_collection_to_dataframe(mongo_uri, db_name, collection_name)
        
        if df is None or df.empty:
            print("No data retrieved from MongoDB.")
            return

        # Assuming the target variable is named 'target' and is binary
        if 'treatment' not in df.columns:
            print("The target column 'treatment' is not present in the DataFrame.")
            return print("data collected successfully")

        X = df.drop(columns=['treatment','Age_Group'], axis=1)
        y = df['treatment'] # target variable

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the CatBoostClassifier
        # taking Best parameters from the model_traning.ipynb file
        model = RandomForestClassifier(bootstrap= True, max_depth= 20, min_samples_leaf= 2, min_samples_split = 5, n_estimators=200) 
        model.fit(X_train, y_train)

        # Save the trained model to a file
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

        print(f"Model trained and saved to {model_path}")

    except Exception as e:
        print(f"An error occurred during training or saving the model: {e}")
        
# python -m src.models.train