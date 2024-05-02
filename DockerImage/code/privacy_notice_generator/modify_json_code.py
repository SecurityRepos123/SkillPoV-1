import os
import json
from path import filter_path
import filter_index_js_repo

final_rewrite_path = filter_index_js_repo.filter_js_file()

def intent_exists(intents, new_intent):
    # Check if the new_intent is already in the intents list
    return any(intent.get("name") == new_intent["name"] for intent in intents)

def modify_json_code():
    # Initialize a set to store unique file names
    unique_file_names = set()

    # Traverse all files in the path
    for repo in final_rewrite_path:
        for root, dirs, files in os.walk(repo):
            for file in files:
                if file.endswith(".json") and file[2] == '-' and len(file) == 10:
                    json_file_path = os.path.join(root, file)
                    unique_file_names.add(json_file_path)
    print(unique_file_names)
    
    # Traverse all json files in the folder
    for json_file in unique_file_names:
        with open(json_file, "r") as f:
            data = json.load(f)
            # Define new intents to be added
            new_intents = [
                {
                    "name": "NoExitIntent",
                    "slots": [],
                    "samples": ["no", "no exit", "exit"]
                },
                {
                    "name": "EnterSkillIntent",
                    "slots": [],
                    "samples": ["yes", "yes continue", "continue", "i don't want to know"]
                },
                {
                    "name": "WantKnowIntent",
                    "slots": [],
                    "samples": [
                        "i want to know"
                    ]
                },
                {
                    "name": "DataCollectionIntent",
                    "slots": [],
                    "samples": [
                        "tell me what data is collected"
                    ]
                }
            ]

            # Get the current list of intents
            current_intents = data.get("interactionModel", {}).get("languageModel", {}).get("intents", [])

            # Loop through new_intents and add each one if it doesn't already exist
            for new_intent in new_intents:
                if not intent_exists(current_intents, new_intent):
                    current_intents.append(new_intent)
                    print(f"Inserted new intent {new_intent['name']} in {json_file}.")
                else:
                    print(f"Intent {new_intent['name']} already exists in {json_file}.")
            
            # Write back the updated json content with the new intents added
            with open(json_file, "w") as f:
                json.dump(data, f, indent=4)