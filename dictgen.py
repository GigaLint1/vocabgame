import requests
import json
import csv

# app id and key from my oxforddictionaryapi
app_id = 'f5dd39d6'
app_key = '9d76bf468e504c40f50eed0ff5f2b713'


def word_dict(word):
    language = 'en-gb'
    word_id = word  # string of word in lower
    # fields = 'pronunciations'
    # strictMatch = 'false'

    url = 'https://od-api.oxforddictionaries.com:443/api/v2/entries/' + language + '/' + word_id.lower()
    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
    mydict = r.json()
    return mydict


def word_info(dict):
    worddict = {'word': dict['word'], 'type': dict['results'][0]['lexicalEntries'][0]['lexicalCategory']['id']}

    defs = []
    egs2 = []

    for senses in dict['results'][0]['lexicalEntries'][0]['entries'][0]['senses']:

        if 'definitions' in senses.keys():
            defs.append(senses['definitions'][0])
            egs1 = []
            try:
                examples = []
                for example in senses['examples']:
                    examples.append(example['text'])
                egs1.append(examples)

            except:
                egs1.append('No examples')
        egs2.append(egs1)

    worddict['definitions'] = defs
    worddict['examples'] = egs2

    return worddict


with open(r'C:\Users\grego\PycharmProjects\Dictionary\words.csv') as words:
    with open(r'C:\Users\grego\PycharmProjects\Dictionary\testing.csv', 'a') as dict:
        fields = ['word', 'type', 'definitions', 'examples']
        reader = csv.DictReader(words)
        writer = csv.DictWriter(dict, fieldnames=fields)
        writer.writeheader()
        for row in reader:
            w = word_dict(row['word'])
            writer.writerow(word_info(w))

# Raison detre
# Raise one's hackles
# Euchred
# At Loggerheads with someone
# Gnash one's teeth
# Nippier
# Disparaged
# Steal a march
# Oppobrium
# Gin something up
