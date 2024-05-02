## generate report for each skill
import csv
from path import results_path

# read results
def read_results(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        outputs = []
        for row in reader:
            outputs.append([filename.split('/')[-1][:-4].replace('_', ' ')] + row)
    return outputs

def get_content_safety(skill_name):
    all_issues = []
    all_issues = all_issues + read_results(results_path + '/' + skill_name + '/content_safety/outputs_data_collection.csv')
    all_issues = all_issues + [['permission data collection', i[2]] for i in read_results(results_path + '/' + skill_name + '/privacy_violation/permissions.csv')]
    return all_issues

def get_report(skill_name):
    all_issues = []
    all_issues = all_issues + get_content_safety(skill_name)
    try:
        all_issues = all_issues
    except:
        all_issues = all_issues + []

    with open(results_path + '/' + skill_name + '/report.txt', 'w') as f:
        for issue in all_issues:
            if issue == '' or issue == ['']:
                continue
            for i in issue:
                x = f.write(i + '\t')
            x = f.write('\n')
        
