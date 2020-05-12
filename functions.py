import re
import csv
import random

def new_word():
    _words = []

    with open('dictionary.csv', 'r') as dictionary:
        reader = csv.DictReader(dictionary, fieldnames=['word', 'type', 'definitions', 'examples'])
        for row in reader:
            _words.append(row)

    word = random.choice(_words[1:])['word']

    for i in _words[1:]:
        if i['word'] == word:
            correctdef = re.sub(r"[(\[\')(\'\])]", ' ', i['definitions'])
            _words.pop(_words.index(i))
    _fakes = random.sample(_words, 2)
    fakedef1 = re.sub(r"[(\[\')(\'\])]", ' ', _fakes[0]['definitions'])
    fakedef2 = re.sub(r"[(\[\')(\'\])]", ' ', _fakes[1]['definitions'])

    return word, correctdef, fakedef1, fakedef2

def new_sentence():
    _sentences = []
    _haveexamples = []
    with open('dictionary.csv', 'r') as dictionary:
        reader = csv.DictReader(dictionary, fieldnames=['word', 'type', 'definitions', 'examples'])
        for row in reader:
            _sentences.append(dict(row))

    for i in _sentences:
        if i['examples'] != "['No examples']":     
            i['examples'] = re.sub(r"[(\[\[)(\]\])]", '', i['examples']).split("', '")
            _haveexamples.append(i)

    _sentence = random.choice(_haveexamples[1:])['examples']       
    if len(_sentence) > 1:
        sentence = " / \n".join(_sentence)
    else:
        sentence = _sentence[0]

    for i in _haveexamples[1:]:
        if i['examples'] == _sentence:
            correctword = i['word']
            _sentences.pop(_sentences.index(i))
            sentence = sentence.replace(correctword, '______').rstrip("\"'").lstrip("\"'")               

    _fakes = random.sample(_sentences[1:], 2)
    fakeword1 = _fakes[0]['word']
    fakeword2 = _fakes[1]['word']  
    return sentence, correctword, fakeword1, fakeword2