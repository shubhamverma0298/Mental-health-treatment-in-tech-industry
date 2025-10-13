import pickle
import pandas as pd
import numpy as np

def load_model(model_path):
    """
    Loads a trained model from a .pkl file.

    Args:
        model_path (str): The path to the saved model file.

    Returns:
        The loaded model object, or None if an error occurs.
    """
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully.")
        return model
    except FileNotFoundError:
        print(f"Error: The file at {model_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None

def make_prediction(model, input_data):
    """
    Makes a prediction using the loaded model.

    Args:
        model: The trained model object.
        input_data (pd.DataFrame): A DataFrame containing the input features for prediction.

    Returns:
        The model's prediction, or None if an error occurs.
    """
    try:
        prediction = model.predict(input_data)
        return prediction
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return None

