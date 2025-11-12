# Optional helper file (for scaling, cleaning, or reusable plots)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_country_data(path, country):
    df = pd.read_csv(path)
    df["country"] = country
    return df
