
import pandas as pd


def load_data(file_path="support_tickets.csv"):
    df = pd.read_csv(file_path)
    df["created_at"] = pd.to_datetime(df["created_at"])
    return df
