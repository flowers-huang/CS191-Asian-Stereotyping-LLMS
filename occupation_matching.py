import pandas as pd
import string

FILENAME = "cleaned_classification_gemini_1.5.csv"

def read_occ_data():
    # OCC Title -- 'OCC_TITLE'
    # Annual Wage -- 'A_mean'
    OCC_data = pd.read_csv("national_M2023_dl-Table 1.csv", thousands=',')

    # Clean up OCC titles
    OCC_data['OCC_TITLE'] = OCC_data['OCC_TITLE'].apply(lambda x : x.translate(str.maketrans('', '', string.punctuation)))
    
    return OCC_data

def read_occupation_ethnicity():
    occupation_ethnicity = pd.read_csv(FILENAME)
    return occupation_ethnicity

def process_occupations(occupation_ethnicity, OCC_data):
    occupation_wages = []

    for index, row in occupation_ethnicity.iterrows():
        # if we cannot find an annual average wage
        print(row['occupation'])
        if OCC_data[OCC_data['OCC_TITLE'].str.contains(row['occupation'])].empty:
            occupation_wages.append(None)
            print("!!")
        else:
            wage = OCC_data[OCC_data['OCC_TITLE'].str.contains(row['occupation'])]['A_MEAN'].tolist()[0]
            print(wage)
            occupation_wages.append(OCC_data[OCC_data['OCC_TITLE'].str.contains(row['occupation'])]['A_MEAN'].tolist()[0])
        
    occupation_ethnicity['A_WAGE'] = occupation_wages

    update_file(FILENAME, occupation_ethnicity)

def update_file(FILENAME, df):
    df.to_csv(FILENAME, mode='w', index=False)


def processing_occupation_wages():
    print("Reading OCC data")
    OCC_data = read_occ_data()
    print("Reading occupation ethnicity data")
    occupation_ethnicity = read_occupation_ethnicity()
    print("Processing occupations")
    process_occupations(occupation_ethnicity, OCC_data)

def calc_average_wage():
    print("Reading occupation ethnicity data")
    occupation_ethnicity = read_occupation_ethnicity()

    occupation_ethnicity = occupation_ethnicity[~occupation_ethnicity['ethnicity'].isnull()]

    print("MEAN")
    print("OVERALL", occupation_ethnicity['A_WAGE'].mean())
    print(occupation_ethnicity.groupby('ethnicity')['A_WAGE'].mean())
    print("MEDIAN")
    print("OVERALL", occupation_ethnicity['A_WAGE'].median())
    print(occupation_ethnicity.groupby('ethnicity')['A_WAGE'].median())

calc_average_wage()

