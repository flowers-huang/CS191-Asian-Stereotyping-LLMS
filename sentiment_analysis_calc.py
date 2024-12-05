import pandas as pd
import csv
from google.cloud import language_v1

FILENAME = 'generation_mistral_7b_instruct_v0.3_sentiment.csv'

# Reads the file and instantiates a plain text document
def read_file(filename):
    print("Reading file", filename)
    # Read CSV file into pandas DataFrame
    df = pd.read_csv(filename, header=0)
    # print(df)
    return df

def analyze(df):
    print("Mean and median of sentiments as a whole")
    print(df["sentiment"].mean(), df["sentiment"].median())

    print("Mean of sentiments of racial group:")
    print(df[["racial_group", "sentiment"]].groupby("racial_group").mean())

    print("Median of sentiments of racial group:")
    print(df[["racial_group", "sentiment"]].groupby("racial_group").median())

df = read_file(FILENAME)
analyze(df)