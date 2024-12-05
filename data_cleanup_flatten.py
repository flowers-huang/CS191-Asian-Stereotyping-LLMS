import csv
import re
import pandas

processed_file = "classification_gpt-4o.csv"
new_filename = "cleaned_classification_gemini_1.5.csv"
separation = 2

def read_file(filename):
    output_pairs = []
    occupation = ""
    line_num = 0
    with open(filename, 'r') as file:
      # Read each line in the file and set up
      for line in file:
        if line_num % separation == 0:
          occupation = re.sub(r'\W+', ' ', line).strip()
        if line_num % separation == 1:
          line = line.lower()
          assigned = False

          if line.find("white") != -1 or line.find("caucasian") != -1 or line.find("european") != -1  or line.find("american") != -1:
            output_pairs.append({'occupation': occupation, 'ethnicity': "Caucasian"})
            assigned = True
          if line.find("asian") != -1 or line.find("chinese") != -1 or line.find("japanese") != -1:
            output_pairs.append({'occupation': occupation, 'ethnicity': "Asian"})
            assigned = True
          if line.find("hispanic") != -1 or line.find("latino") != -1 or line.find("latinx") != -1:
            output_pairs.append({'occupation': occupation, 'ethnicity': "Hispanic"})
            assigned = True
          if line.find("black") != -1 or line.find("african") != -1:
            output_pairs.append({'occupation': occupation, 'ethnicity': "African"})
            assigned = True
          if line.find("middle eastern") != -1:
            output_pairs.append({'occupation': occupation, 'ethnicity': "Middle Eastern"})
            assigned = True
          if line.find("islander") != -1 or line.find("pacific islander") != -1:
            output_pairs.append({'occupation': occupation, 'ethnicity': "Pacific Islander"})
            assigned = True
          
          if not assigned:
            print("Missing occupation ", occupation, "with response", line)
            output_pairs.append({'occupation': occupation, 'ethnicity': "None"})

          occupation = ""

        line_num += 1

    #print(output_pairs)    
    return output_pairs

def write_to_file(filename = "temp.csv", input_data = []):
  with open(filename, 'a', newline='') as csvfile:
    fieldnames = ['occupation', 'ethnicity']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(input_data)

def file_cleanup():
  print("Reading File")
  output_pairs = read_file(processed_file)
  print("Found output pairs, now writing")
  write_to_file(filename=new_filename, input_data=output_pairs)

def process_csv(csv_file):
  print(csv_file)
  csvFile = pandas.read_csv(csv_file)
  print(csvFile["ethnicity"].value_counts())
  print(csvFile.isna().sum())

def clean_file_counts(csv_file):
  print("Reading File")
  process_csv(csv_file)
    
def main():
  clean_file_counts(new_filename)

main()