import pandas as pd
import csv
from google.cloud import language_v1

FILENAME = 'generation_mistral_7b_instruct_v0.3.csv'
RESULT_FILENAME = 'generation_mistral_7b_instruct_v0.3_sentiment.csv'

# Reads the file and instantiates a plain text document
def read_file(filename):
    print("Reading file", filename)
    # Read CSV file into pandas DataFrame
    df = pd.read_csv(filename, header=0)
    # print(df)
    return df

def process(df):
    print("Processing Sentiments")
    sentiments = []

    responses = df['response'].tolist()

    for response in responses:
        sentiments.append(analyze(response))
    
    df["sentiment"] = sentiments

    # print(df["sentiment"])
    write_to_file(df)

def write_to_file(df):
    print("Writing to file")
    column_list=["racial_group", "sentiment"]
    df.to_csv(RESULT_FILENAME, columns = column_list, index=False)


def analyze(content):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language_v1.LanguageServiceClient()

    # Convert to document
    document = language_v1.Document(
        content=content, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    annotations = client.analyze_sentiment(request={"document": document})

    # Print the results
    #print_result(annotations)
    score = annotations.document_sentiment.score
    return score

def print_result(annotations):
    score = annotations.document_sentiment.score
    # magnitude = annotations.document_sentiment.magnitude

    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        print(f"Sentence {index} has a sentiment score of {sentence_sentiment}")

    # print(f"Overall Sentiment: score of {score} with magnitude of {magnitude}")
    return 0

def main():
    dataframe = read_file(FILENAME)
    process(dataframe)

main()