import itertools
import json

def hamdist(str1, str2):
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
            if ch1 != ch2:
                    diffs += 1
    return diffs

def hamdistOnPairs(json):
    diff = {}
    for pair in itertools.product(json, repeat=2):
        key = pair
        diff.update({key: hamdist(pair[0], pair[1])})
    return diff

#load json into dictionary
dictPath = 'Dictionaries/master_dictionary.json'
with open(dictPath) as json_data:
    d = json.load(json_data)

#find maximum length word
mx = 0
for x in d:
    if mx < len(x):
        mx = len(x)

#group words by equal length
words = [[] for i in range(mx)]
for x in d:
    words[len(x)-1].append(x)

#go through each pair of words with same length
for i in range(4, 5):
    for j in range(len(words[i])):
        for k in range(j+1, len(words[i])):
            hmd = hamdist(words[i][j], words[i][k])

print(hmd)
