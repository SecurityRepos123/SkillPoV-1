import os
from path import filter_path, chatGPT_path, add_intent_path
import filter_index_js_repo

final_rewrite_path = filter_index_js_repo.filter_js_file()
# find first bracket after "const Launch"
def find_bracket_after_specific_string(code, specific_string):
    start_index = code.find(specific_string)
    
    if start_index != -1:
        bracket_index = code.find("{", start_index)
        
        if bracket_index != -1:
            return bracket_index
        
    return -1

# find matching bracket of first bracket after "const Launch"
def find_matching_bracket(code, start_index):
    stack = []
    for i in range(start_index, len(code)):
        if code[i] == '{':
            stack.append(i)
            # print(stack)
        elif code[i] == '}':
            if not stack:
                return i
            stack.pop()
            if not stack:
                return i
    return -1

# replace with EnterSkillIntent    
def replace_launch_request(code):
    if code.find("Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest'") != -1:
        replace_code = code.replace(
            "Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest'",
            "handlerInput.requestEnvelope.request.type === 'IntentRequest' && handlerInput.requestEnvelope.request.intent.name === 'EnterSkillIntent'")
        return replace_code
    if code.find("handlerInput.requestEnvelope.request.type === 'LaunchRequest'") != -1:
        replace_code = code.replace(
            "handlerInput.requestEnvelope.request.type === 'LaunchRequest'",
            "handlerInput.requestEnvelope.request.type === 'IntentRequest' && handlerInput.requestEnvelope.request.intent.name === 'EnterSkillIntent'")
        return replace_code

# add new IntentHandlers    
def add_exports_handler(code):
    new_handlers = """
    NoExitIntentHandler,
    EnterSkillIntentHandler,
    WantKnowIntentHandler,
    DataCollectionIntentHandler,"""

    add_handlers_start = code.find("addRequestHandlers(")
    add_handlers_end = find_matching_bracket(code, add_handlers_start + len("addRequestHandlers("))

    modified_code = code[:add_handlers_start + len("addRequestHandlers(")] + new_handlers + code[add_handlers_start + len("addRequestHandlers("):add_handlers_end] + code[add_handlers_end:]

    return modified_code

# replace code and overwite old file
def replace_code(input_file, output_file, replace_content):
    with open(input_file, 'r') as file:
        js_code = file.read()
    if js_code:
        launch_handler_start_pre = js_code.find("const Launch")
        launch_handler_start = find_bracket_after_specific_string(js_code, "const Launch")
        launch_handler_end = find_matching_bracket(js_code, launch_handler_start)

        with open(add_intent_path, 'r') as file:
            new_content = file.read()
            speak_output_content = new_content.replace("{repalce_content}", replace_content)
            # print(speak_output_content)

        if launch_handler_start_pre != -1 and launch_handler_end != -1:
            replace_code = replace_launch_request(js_code)
            launch_handler_code_new = (replace_code[:launch_handler_start_pre] + '\n' + 
                                       speak_output_content + 
                                       '\n' + "const EnterSkillIntentHandler = " + 
                                       replace_code[launch_handler_start:])
            add_exports_handler_code = add_exports_handler(launch_handler_code_new)

            with open(output_file, 'w') as output_file:
                output_file.write(add_exports_handler_code)
            return True
        else:
            return False

def search_and_replace():
    found_count = 0
    not_found_count = 0
    for repo in final_rewrite_path:
        for dirpath, dirnames, filenames in os.walk(repo):
            if "lambda" in dirnames:
                lambda_dir = os.path.join(dirpath, "lambda")
                for root, dirs, files in os.walk(lambda_dir):
                    parts = root.split('/')
                    try:
                        dataset_index = parts.index('dataset')
                        repos_index = parts.index('repos')
                    except ValueError:
                        print("One of the specified elements was not found.")
                    if repos_index - dataset_index == 1:
                        author_path = parts[repos_index + 1]
                        skill_path = parts[repos_index + 2]
                    else:
                        print("The elements 'dataset' and 'repos' are not in the expected sequence.")
                    replace_path = chatGPT_path + "/" + author_path + "/" + skill_path + "/" + "report.txt"
                    try:
                        with open(replace_path, 'r') as file:
                            replace_content = file.read()
                    except FileNotFoundError:
                        print(f"File {replace_path} not found. Skipping...")
                        replace_content = None
                    #print(replace_content)
                    for file in files:
                        if file == "index.js":
                            # print(root, file)
                            try:
                                result = replace_code(os.path.join(root, file), os.path.join(root, "index_new.js"), replace_content)
                                if result:
                                    found_count += 1
                                else:
                                    not_found_count += 1
                            except TypeError as e:
                                print(f"TypeError: {e}")
    print("found_count: ", found_count, "not_found_count: ", not_found_count)