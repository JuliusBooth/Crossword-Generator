import json


DICTIONARY = "../Dictionaries/master_dictionary.json"
with open(DICTIONARY, "r") as read_file:
    words = json.load(read_file)
    words = dict([(k.upper(),v) for (k,v) in words.items()])

search_term = "".upper()
indices=[(1,"H"), (4,"M")]
word_length = 6

for word, v in words.items():
    length = len(word)
    ok = True
    if length == word_length and search_term in word:
        for num, letter in indices:
            if word[num-1] != letter:
                ok= False
        if ok:
            print(word)
