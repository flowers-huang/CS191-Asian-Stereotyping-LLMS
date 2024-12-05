import csv

filename = "generation_gpt-4o.csv"

def read_groups():
  ethnic_groups = []
  with open("race_ethnic_groups.txt", 'r') as file:
      # Read each line in the file and set up
      for line in file:
          ethnic_groups.append(line.strip())
    
  return ethnic_groups

def calculate_lengths(filename):
    ethnic_groups = read_groups()
    total_lengths = {}

    for ethnic_group in ethnic_groups:
        total_lengths[ethnic_group] = 0

    response_counter = 0

    with open(filename, mode ='r')as file:
        csvFile = csv.reader(file)
        heading = next(csvFile) # skip header

        for lines in csvFile:
            ethnic_group = lines[0]
            response = lines[1]

            total_lengths[ethnic_group] += len(response)

            response_counter += 1

    num_questions = response_counter / len(ethnic_groups)

    return num_questions, total_lengths

def average_lengths(num_questions, total_lengths):
    avg_lengths = {}
    for key in total_lengths:
        avg_lengths[key] = total_lengths[key] / num_questions

    return avg_lengths

def main():
    num_questions, total_lengths = calculate_lengths(filename)
    avg_lengths = average_lengths(num_questions, total_lengths)

    print("There were a total of", num_questions, "questions.")
    print("The following were the total lengths of the responses taken from the file", filename)
    print(total_lengths)
    print("The following were the average lengths of the responses taken from the file", filename)
    print(avg_lengths)

main()