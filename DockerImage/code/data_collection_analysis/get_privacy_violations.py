import csv
import json
from path import results_path

### read content from manifest file

def get_manifest_content(skill):
    content = {}
    try:
        mainfest = json.loads(open(skill['manifest_file']).read())
    except:
        return {}
    if 'manifest' in mainfest:
        content = mainfest['manifest']
    elif 'skillManifest' in mainfest:
        content = mainfest['skillManifest']
    return content


def get_permission(skill):
    content = get_manifest_content(skill)
    try:
        permissions = content['permissions']
    except:
        permissions = []
    return [permission['name'] for permission in permissions]

# read all the results
def read_results(filename):
    with open(results_path + '/' + filename) as f:
        reader = csv.reader(f)
        results = []
        for row in reader:
            results.append(row)
    return results

# read collected data and check whether privacy policy is complete
def get_data_collection_in_output(skill_name, skill):
    output_data_collection = read_results(skill_name + '/content_safety/outputs_data_collection.csv')
    data_collected_in_output = []
    for output in output_data_collection:
        filename, output, data_type = output
        data_collected_in_output.append(data_type[13:])
    return data_collected_in_output

def write_results(filename, outputs):
    with open(results_path + '/' + filename, 'a', newline = '') as f: 
        writer = csv.writer(f)
        for output in outputs:
            x = writer.writerow(output)

def get_data_collection_in_permission(skill_name, skill):
    permission_mapping = {}
    permission_mapping['alexa::devices:all:address:full:read'] = 'address'
    permission_mapping['alexa:devices:all:address:country_and_postal_code:read'] = 'postal code'
    permission_mapping['alexa::profile:name:read'] = 'name'
    permission_mapping['alexa::profile:given_name:read'] = 'name'
    permission_mapping['alexa::profile:email:read'] = 'email'
    permission_mapping['alexa::profile:mobile_number:read'] = 'number'
    permission_mapping['alexa::devices:all:geolocation:read'] = 'location'
    permission_asked = get_permission(skill)
    data_collected_in_permission = []
    for permission in permission_asked:
        if permission in permission_mapping:
            data_collected_in_permission.append(('skills.json', permission_mapping[permission]))
    write_results(skill_name + '/privacy_violation/permissions.csv', data_collected_in_permission)

def get_privacy_violations(skill_name):
    skill = json.loads(open(results_path + '/' + skill_name + '/skill.json').read())
    get_data_collection_in_permission(skill_name, skill)