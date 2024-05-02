import os
import openai
from path import final_path, data_collection_results_path

def chatgpt_summarize(content, folder_path, filename):
    # place your openai api key here
    openai.api_key = ''
    messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
    message = "If my input is 'data collection during conversation: birthday, data collection during conversation: age, data collection during conversation: address, ', \
               Your ouptut should be 'This skill will collect your birthday, age and address during the conversation.'\
               If my input is 'data collection during conversation: name, ', \
               Your ouptut should be 'This skill will collect your name during the conversation.'\
               If my input is 'permission data collection: name, '. \
               Your ouptut should be 'This skill will seek your name permission.'\
               If my input is 'permission data collection: name, permission data collection: email, permission data collection: age, '. \
               Your ouptut should be 'This skill will seek your name, email and age permissions.'\
               If my input is 'data collection during conversation: name, permission data collection: name, ', \
               Your ouptut should be 'This skill will collect your name during the conversation. Also, this skill will seek your name permission.'\
               If my input is 'data collection during conversation: birthday, data collection during conversation: age, data collection during conversation: name, permission data collection: name, permission data collection: phone number, permission data collection: email, '\
               Your ouptut should be 'This skill will collect your birthday, age and name during the conversation. Also, this skill will seek your name, phone number and email permissions.'\
               Please remember above rules. The input is as follows: " + content
    # print("Input: " + message)
    
    max_retries = 3  
    retry_count = 0

    while retry_count < max_retries:
        try:
            if message:
                messages.append(
                    {"role": "user", "content": message},
                )
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages, timeout=30
                )
            reply = chat.choices[0].message['content']
            # print("chaGPT: " + reply)
            components = filename.split("~~")
            print(components)
            file_path = folder_path + "/" + "chatGPT/" + components[0] + "/" + components[1] + "/" + components[2]
            os.makedirs(folder_path + "/" + "chatGPT/" + components[0] + "/" + components[1], exist_ok=True)
            with open(file_path, 'w') as file:
                #print(file_path)
                file.write(reply)
            break
        except openai.error.Timeout as e:
            print(f"An error occurred: {e}. Retrying...")
            retry_count += 1

def generate_chatgpt_output():
    for filename in os.listdir(final_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(final_path, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                chatgpt_summarize(content, data_collection_results_path, filename)
