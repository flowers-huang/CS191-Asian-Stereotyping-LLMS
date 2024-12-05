import os
import csv
from tqdm import tqdm
from together import Together
import google.generativeai as genai
import time
from openai import OpenAI


client = Together(api_key="REMOVED")
genai.configure(api_key="REMOVED")

openai_client = OpenAI(api_key = "REMOVED")

models = ["meta-llama/Llama-3.2-3B-Instruct-Turbo", "mistralai/Mistral-7B-Instruct-v0.3", "gemini_1.5", "gpt-4o"]

### Function defs
def set_up_messages(database_file = None, ethnic_groups = ["Asian"], verbose=False):
  if database_file is None:
    return ["What model are you?"]
  else:
    completed_statements = []

    with open(database_file, 'r') as file:
      # Read each line in the file and set up
      for line in file:
          db_statement = line.strip()
          for ethnic_group in ethnic_groups:
            completed_statement = db_statement.replace("____", ethnic_group)
            completed_statements.append([ethnic_group, completed_statement])
  
  if verbose:
     print(completed_statements)
  
  return completed_statements

def read_groups():
  ethnic_groups = []
  with open("race_ethnic_groups.txt", 'r') as file:
      # Read each line in the file and set up
      for line in file:
          ethnic_groups.append(line.strip())
    
  return ethnic_groups

def write_to_file(filename = "temp.csv", input_data = []):
  with open(filename, 'a', newline='') as csvfile:
    fieldnames = ['racial_group', 'response']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(input_data)

### TO CHANGE HERE!!!
curr_model = models[3]
show_statements = False
database_file = "questions_sub_answer.txt"
output_file = "questions_sub_answer_gpt-4o.csv"
ethnic_groups = read_groups()
#ethnic_groups = ["Asian"]

def main():
  print("Beginning experiment...")
  print("Current model will be:")
  print(curr_model)
  print()

  print("Set up messages")
  msgs = set_up_messages(database_file=database_file, ethnic_groups=ethnic_groups, verbose=show_statements)
  output_data = []

  print("Processing Responses")

  # These are together.apis
  if curr_model == models[0] or curr_model == models[1]: 
    for i in tqdm(range(len(msgs))):
      msg = msgs[i]
      response = client.chat.completions.create(
        model=curr_model,
        messages=[{"role": "user", "content": msg[1]}],
      )

      response = response.choices[0].message.content

      output_data.append({'racial_group': msg[0], 'response': response})
  elif curr_model == models[2]:
    model = genai.GenerativeModel("gemini-1.5-flash")

    for i in tqdm(range(len(msgs))):
      msg = msgs[i]
      response = model.generate_content(msg[1])

      output_data.append({'racial_group': msg[0], 'response': response.text})

      time.sleep(3) # Sleep for 3 seconds
  else:
    for i in tqdm(range(len(msgs))):
      msg = msgs[i]
      chat = openai_client.chat.completions.create(
              model="gpt-4o", 
              messages=[
                  {"role": "system", "content": "You are a helpful assistant."},
                  {
                      "role": "user",
                      "content": msg[1]
                  }
              ]
          )
      reply = chat.choices[0].message.content

      output_data.append({'racial_group': msg[0], 'response': reply})

  print("Writing to file...")
  write_to_file(filename = output_file, input_data = output_data)
  print("All done!")

main()