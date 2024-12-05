import csv

def write_to_file(filename = "occupations_cleaned.txt", input_data = []):
  with open(filename, 'a', newline='') as file:
    for input in input_data:
        file.write(input)
    file.close

def read_occupations():
    occupations = []
    with open("occupations.txt", 'r') as file:
        # Read each line in the file and set up
        for line in file:
            if "-" not in line and "/" not in line: 
                if line not in occupations:
                    occupations.append(line)
        
    return occupations

def main():
  occupations = read_occupations()
  write_to_file(input_data = occupations)


main()