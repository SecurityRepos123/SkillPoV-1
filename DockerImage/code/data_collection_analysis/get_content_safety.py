import re
import csv
import spacy
import string
from path import results_path

nlp = spacy.load("en_core_web_sm")

# read all the outputs
def read_skill_outputs(skill_name):
    with open(results_path + '/' + skill_name + '/content_safety/outputs.csv') as f:
        reader = csv.reader(f)
        outputs = []
        for row in reader:
            outputs.append(row)
    return outputs

def write_results(filename, outputs):
    with open(results_path + '/' + filename, 'w', newline = '') as f: 
        writer = csv.writer(f)
        for output in outputs:
            x = writer.writerow(output)

def get_data_collection_outputs(outputs):
    noun = ['address', 'name', 'email', 'email address', 'birthday', 'age', 'gender', 'location', 'contact', 'phonebook', 'profession', 'income', 'ssn', 'zipcode', 'ethnicity', 'affiliation', 'orientation', 'affiliation', 'postal code', 'zip code', 'first name', 'last name', 'full name', 'phone number', 'social security number', 'passport number', 'driver license', 'bank account number', 'debit card number']
    noun2 = [word.split()[-1] for word in noun]
    add_sentences = {"how old are you": 'age', "when were you born": 'age', "where do you live":'location' ,"where are you from": 'location', "what can i call you": 'name', 'male or female': 'gender', 'what city do you live in?': 'location'}
    words = ['companion app', 'alexa app', 'amazon.com', 'permission', 'enable', 'grant']
    skills = []
    for output in outputs:
        filename, output = output
        output = output.lower()
        if 'you' not in output:
            continue
        if ' ' not in output:
            continue
        sentences = re.split(r' *[\n\,\.!][\'"\)\]]* *', output)
        for sentence in sentences:
            if any (word in output for word in words):
                continue
            if any ('your ' + word + ' is' in sentence for word in noun):
                continue
            if any (word in sentence for word in noun) and 'your' in sentence:
                doc = nlp(sentence)
            for word in noun:
                if word not in sentence or 'your' not in sentence:
                    continue
                if word == 'name' and 'your name' not in sentence:
                    continue
                if word == 'address' and 'email address' in sentence:
                    continue
                if word == 'phone number' and 'dial your local emergency' in sentence:
                    continue
                for l in doc:
                    if l.text == 'your' and l.head.text in noun2 and l.head.text in word:
                        if 'name' in word:
                            skills.append((filename, output, 'collect data name'))
                        else:
                            skills.append((filename, output, 'collect data ' + word))
            for sent in add_sentences:
                    if sent in sentence.translate(str.maketrans('', '', string.punctuation)):
                        skills.append((filename, output, 'collect data ' + add_sentences[sent]))
    return set(skills)


def get_skill_data_collection_in_outputs(skill_name, outputs):
    data_collection_outputs = get_data_collection_outputs(outputs)
    write_results(skill_name + '/content_safety/outputs_data_collection.csv', data_collection_outputs)

def get_content_safety(skill_name):
    outputs = read_skill_outputs(skill_name)
    outputs = outputs 
    get_skill_data_collection_in_outputs(skill_name, outputs)