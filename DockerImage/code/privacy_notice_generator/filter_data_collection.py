import os
from path import data_collection_results_path, results_path

def filter_lines(input_file, output_file):
    check_file = os.stat(input_file).st_size
    if (check_file != 0):
        with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:
            for line in in_file:
                if "outputs data collection" in line:
                    index = line.find("collect data")
                    if index != -1:
                        collected_data = line[index + len("collect data"):].strip()
                        out_file.write("data collection during conversation: " + collected_data + "\n")
                if "permission data collection" in line:
                    index = line.find("permission data collection")
                    if index != -1:
                        collected_data = line[index + len("permission data collection"):].strip()
                        out_file.write("permission data collection: " + collected_data + "\n")

def get_author_skill(folder):
    components = folder.split("~") 
    last_two_parts = components[-2:] # get the last two parts: author and skill 
    author = last_two_parts[0]
    skill = last_two_parts[1]
    # print(last_two_parts, author, skill)
    return data_collection_results_path + "/final/" + author + "~~" + skill + "~~report.txt"

def delete_empty_files():
    for root, dirs, files in os.walk(data_collection_results_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) == 0:
                os.remove(file_path)

def remove_duplicates(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    unique_lines = list(set(lines))
    
    with open(input_file, 'w') as file:
        file.writelines(unique_lines)

def reorder_lines(pre_file):
    with open(pre_file, 'r') as file:
        content = file.read()

    parts = content.split(", ")
    data_collection_during_conversation = [part for part in parts if "data collection during conversation" in part]
    for part in data_collection_during_conversation:
        parts.remove(part)
    new_content = ", ".join(data_collection_during_conversation + parts)

    with open(pre_file, 'w') as file:
        file.write(new_content)
    
def get_final_report():
    sub_folders = [name for name in os.listdir(results_path) if os.path.isdir(os.path.join(results_path, name))]
    
    for sub_folder in sub_folders:
        report_file = (results_path+"/"+sub_folder+"/report.txt")
        report_filter_file = get_author_skill(sub_folder)
        try:
            filter_lines(report_file, report_filter_file)
            remove_duplicates(report_filter_file)
            with open(report_filter_file, 'r') as file:
                content = file.read().replace('\n', ', ')
            with open(report_filter_file, 'w') as file:
                file.write(content)
            reorder_lines(report_filter_file)
        except FileNotFoundError:
            pass
    delete_empty_files()