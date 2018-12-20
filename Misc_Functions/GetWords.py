import json


DICTIONARY = "../Dictionaries/master_dictionary.json"
with open(DICTIONARY, "r") as read_file:
    words = json.load(read_file)
    words = dict([(k.upper(),v) for (k,v) in words.items()])

search_term = "friday".upper()

for word, v in words.items():
    length = len(word)
    if length == 14 and search_term in word:
        print(word)
