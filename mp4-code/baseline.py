"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""

def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    # {(word,tag) : count}
    tagCount = {}
    for sentence in train:
        for pair in sentence:
            unknownPair = ("UNK", pair[1])
            if pair in tagCount:
                tagCount[pair] = tagCount[pair] + 1
            else:
                tagCount[pair] = 1
            if unknownPair in tagCount:
                tagCount[unknownPair] = tagCount[unknownPair] + 1
            else:
                tagCount[unknownPair] = 1
    #word to tag
    mostCommonTag = {}
    for pair in tagCount:
        word = pair[0]
        tag = pair[1]
        if word in mostCommonTag:
            currentTag = mostCommonTag[word]
            currentMax = tagCount[(word, currentTag)]
            if tagCount[pair] > currentMax:
                mostCommonTag[word] = tag
        else:
            mostCommonTag[word] = tag
    predictedTag = []
    for sentence in test:
        currentSentence = []
        for word in sentence:
            if word == "START":
                pair = (word, "START")
                currentSentence.append(pair)
            elif word in mostCommonTag:
                pair = (word, mostCommonTag[word])
                currentSentence.append(pair)
            else:
                pair = (word, mostCommonTag["UNK"])
                currentSentence.append(pair)
        predictedTag.append(currentSentence)
    return predictedTag
