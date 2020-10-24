import math
import numpy as np
"""
Part 4: Here should be your best version of viterbi,
with enhancements such as dealing with suffixes/prefixes separately
"""

def viterbi_1(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    # alpha is smoothing parameter
    alpha = 0.0001
    init_prob = math.log(0.0001)
    # how often does t_b follows t_a {(tag_a, tag_b) : prob}
    transition_prob = {}
    # how often word yields tag {(word, tag) : prob}
    emission_prob = {}
    # tag freq {tag : freq}
    tag_freq = {}
    # freq of tags used for transition_prob {(tag_a, tag_b) : freq}
    tag_follow_freq = {}
    # freq of words
    word_freq = {}
    # freq of (word, tag) {(word, tag) : freq}
    word_tag_freq = {}
    # calculate freq of (word ,tag):
    for sentence in train:
        for pair in sentence:
            if pair in word_tag_freq:
                word_tag_freq[pair] = word_tag_freq[pair] + 1
            else:
                word_tag_freq[pair] = 1

    for sentence in train:
        for pair in sentence:
            tag = pair[1]
            if tag in tag_freq:
                tag_freq[tag] = tag_freq[tag] + 1
            else:
                tag_freq[tag] = 1
    #count unique amoutn fo tag for word
    unique_tag_per_word = {}
    for pair in word_tag_freq:
        if pair[1] in unique_tag_per_word:
            unique_tag_per_word[pair[1]] += 1
        else:
            unique_tag_per_word[pair[1]] = 1

    # calculating tag_follow_freq
    for sentence in train:
        for i in range(len(sentence) - 1):
            tag_a = sentence[i][1]
            tag_b = sentence[i + 1][1]
            pair = (tag_a, tag_b)
            if pair in tag_follow_freq:
                tag_follow_freq[pair] = tag_follow_freq[pair] + 1
            else:
                tag_follow_freq[pair] = 1

    # calculate transition prob
    for tag_pair in tag_follow_freq:
        tag_a_freq = tag_freq[tag_pair[0]]
        # prob_of_pair = tag_follow_freq[tag_pair] / tag_a_freq
        prob_of_pair = (tag_follow_freq[tag_pair] + alpha) /(tag_a_freq + alpha * (1 + unique_tag_per_word[tag_pair[0]]))
        transition_prob[tag_pair] = math.log(prob_of_pair)
    # calculate freq of words
    for sentence in train:
        for pair in sentence:
            word = pair[0]
            if word in word_freq:
                word_freq[word] = word_freq[word] + 1
            else:
                word_freq[word] = 1

    # calculate word_all_tag_prob
    # will contain the prob of {(word, tag) : prob}
    word_all_tag_prob = {}
    for sentence in train:
        for pair in sentence:
            word = pair[0]
            tag = pair[1]
            count_word_pair = word_tag_freq[pair]
            pair_prob = (count_word_pair + alpha) / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
            word_all_tag_prob[pair] = math.log(pair_prob)


    emission_prob = word_all_tag_prob

    tags = []

    for tag in tag_freq:
        tags.append(tag)

    answer = []
    for sentence in test:
        rows = len(sentence)  # word_idx
        cols = len(tags) # tag_idx
        v = [[0 for x in range(cols)] for y in range(rows)] #holds probs
        b = [[0 for x in range(cols)] for y in range(rows)] #holds respective tags
        for word_idx in range(rows):
            for tag_idx in range(cols):
                tag = tags[tag_idx]
                word = sentence[word_idx]
                if word_idx == 0:
                    if (word,tag) not in emission_prob:
                        prob = alpha / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
                        emission_prob[(word,tag)] = -100
                        # emission_prob[(word,tag)] = math.log(prob)
                    v[word_idx][tag_idx] =  init_prob + emission_prob[(word, tag)]
                else:
                    internal_counter = 0
                    curr_max_prob = -999999999999
                    curr_best_tag = ""

                    for prev_tag in tags:
                        if (word, tag) not in emission_prob:
                            prob = (0 + alpha) / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
                            emission_prob[(word,tag)] = -100
                            # emission_prob[(word,tag)] = math.log(prob)
                        if (prev_tag, tag) not in transition_prob:
                            transition_prob[(prev_tag, tag)] = -100000000

                        prev_v = v[word_idx - 1][internal_counter]
                        transition_probability = transition_prob[(prev_tag, tag)]
                        emission_probability = emission_prob[(word, tag)]
                        curr_looking_prob = prev_v + transition_probability + emission_probability

                        if (curr_looking_prob > curr_max_prob):
                            curr_max_prob = curr_looking_prob
                            curr_best_tag = prev_tag

                        internal_counter += 1

                    v[word_idx][tag_idx] = curr_max_prob
                    b[word_idx][tag_idx] = curr_best_tag
        #backtrace reference from https://en.wikipedia.org/wiki/Viterbi_algorithm
        ret_sentence = []
        col_index_to_use = 0
        max = -999999999999
        #find where to start
        for i in range(cols):
            if v[-1][i] > max:
                max = v[-1][i]
                col_index_to_use = i

        first_iter = True
        for i in range(rows - 2, -1, -1):
            if first_iter:
                ret_sentence.append(("END","END"))
                first_iter = not first_iter
            ret_sentence.append((sentence[i], b[i + 1][col_index_to_use]))
            col_index_to_use = tags.index(b[i + 1][col_index_to_use])

        # ret_sentence.append(("START", "START"))

        ret_sentence.reverse()
        answer.append(ret_sentence)


    return answer
