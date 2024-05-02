import os
import time
from tqdm import tqdm
import generate_skill_index
import get_skill_outputs
import get_content_safety
import get_privacy_violations
import generate_report
import os
import shutil
from path import repo_path, results_output_path, results_path, data_set_path

def check_skill(root_path, folder):
    time0 = time.time()
    print('\nFinding skills...\n')
    try:
        skills = generate_skill_index.generate_skill_index(root_path + '/' + folder)
    except:
        return None
    if skills == []:
        return None
   
    for skill in skills:
        skill_name = skill['root'].replace('/', '~').replace(' ', '@')
        if os.path.isfile(results_path + '/' + skill_name + '/report.txt'):
            continue
        print(skill_name)
        get_skill_outputs.get_all_outputs(skill_name)
        get_content_safety.get_content_safety(skill_name)
        get_privacy_violations.get_privacy_violations(skill_name)
        generate_report.get_report(skill_name)

def main(root_path, multi_skills = 0):
    # each folder means one author, one folder might have several skills
    x = os.system('mkdir ' + results_path)
    root_path = os.path.abspath(root_path)
    if multi_skills == '1':
        folders = os.listdir(root_path)
        folders.sort()
        for folder in tqdm(folders):
            check_skill(root_path, folder)  
    else:
        check_skill(root_path, '')

if __name__ == "__main__":
    if os.path.exists(results_path):
        shutil.rmtree(results_path)
    main(repo_path, 1)
