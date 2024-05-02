import re
import csv
import json
from path import results_path

def remove_comments(lines):
    commented = 0
    new_lines = []
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        if line[0] == '#' or line[:2] == '//':
            continue
        if line[:3] == '\'\'\'' or line[:3] == '"""' or line[:2] == '/*':
            commented = 1
        if line[-3:] == '\'\'\'' or line[-3:] == '"""' or line[-2:] == '*/':
            commented = 0
            continue
        if commented == 1:
            continue
        new_lines.append(line)
    return new_lines


def get_lines_outputs(lines):
    outputs = []
    for line in lines:
        outputs = outputs + re.findall('\'([^\']*)\'', line.replace('\'s', ' is'))
        outputs = outputs + re.findall('"([^"]*)"', line)
        outputs = outputs + re.findall('`([^`]*)`', line)
    outputs = list(set(outputs))
    return outputs


def get_file_outputs(filename):
    try:
        lines = open(filename).read().split('\n')[:-1]
    except:
        return []
    lines = remove_comments(lines)
    outputs = get_lines_outputs(lines)
    outputs = [(filename, output) for output in outputs]
    outputs_with_sentence_or_website = []
    for output in outputs:
        filename, output = output
        if len(output) > 500:
            continue
        if ' ' in output or 'http' in output:
            outputs_with_sentence_or_website.append((filename, output))
    return outputs_with_sentence_or_website

def write_results(filename, outputs):
    with open(results_path + '/' + filename, 'w', newline = '') as f: 
        writer = csv.writer(f)
        for output in outputs:
            x = writer.writerow(output)

# get all skill outputs string from code (also need to wait for later website and media outputs)
def get_skill_outputs(skill):
    outputs = []
    for file in skill['code_files']:
        outputs = outputs + get_file_outputs(file)
    skill_name = skill['root'].replace('/', '~').replace(' ', '@')
    write_results(skill_name + '/content_safety/outputs.csv', outputs)

# read all the outputs
def read_skill_outputs(skill_name):
    with open(results_path + '/' + skill_name + '/content_safety/outputs.csv') as f:
        reader = csv.reader(f)
        outputs = []
        for row in reader:
            outputs.append(row)
    return outputs

def get_all_outputs(skill_name):
    skill = json.loads(open(results_path + '/' + skill_name + '/skill.json').read())
    get_skill_outputs(skill)
    outputs = read_skill_outputs(skill_name)