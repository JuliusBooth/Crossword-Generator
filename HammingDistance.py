import json

def hamdist(str1, str2):
    dist = 0
    word_length = len(str1)
    for i in range(word_length):
        if str1[i] != str2[i]:
            dist += 1
    return dist


def maxMinHammingDistance():
    # load json into dictionary
    dictPath = 'Dictionaries/master_dictionary.json'
    with open(dictPath) as json_data:
        d = json.load(json_data)
    # group words by equal length
    word_lists = [[] for i in range(20)]
    for word in d:
        if len(word) <= 20:
            word_lists[len(word) - 1].append(word)

    results = {}
    start=12
    for word_length in range(start,start+1):
        word_list = word_lists[word_length-1]

        max_min_distance = 0
        champ_word = ""
        # go through each pair of words with same length
        for i in range(len(word_list)):
            min_distance = word_length+1

            for j in range(len(word_list)):
                if i == j:
                    continue
                distance = hamdist(word_list[i], word_list[j])

                if distance < min_distance:
                    min_distance = distance

            if min_distance > max_min_distance:
                max_min_distance = min_distance
                champ_word = word_list[i]
        results[word_length] = (max_min_distance, champ_word)
        print(word_length, max_min_distance, champ_word)

maxMinHammingDistance()


