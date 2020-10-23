import math
import numpy as np
"""
Part 4: Here should be your best version of viterbi,
with enhancements such as dealing with suffixes/prefixes separately
"""

def viterbi_3(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    alpha = 0.00001
    init_prob = math.log(0.0001)
    # how often does t_b follows t_a {(tag_a, tag_b) : prob}
    transition_prob = {}
    # how often word yields tag {word : tag}
    emission_prob = {}
    # tag freq {tag : freq}
    tag_freq = {}
    # freq of tags used for transition_prob {(tag_a, tag_b) : freq}
    tag_follow_freq = {}
    # freq of words
    word_freq = {}
    # freq of (word, tag) {(word, tag) : freq}
    word_tag_freq = {}
    for sentence in train:
        for pair in sentence:
            tag = pair[1]
            if tag in tag_freq:
                tag_freq[tag] = tag_freq[tag] + 1
            else:
                tag_freq[tag] = 1

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
        prob_of_pair = tag_follow_freq[tag_pair] / tag_a_freq
        transition_prob[tag_pair] = math.log(prob_of_pair)
    # calculate freq of words
    for sentence in train:
        for pair in sentence:
            word = pair[0]
            if word in word_freq:
                word_freq[word] = word_freq[word] + 1
            else:
                word_freq[word] = 1

    # calculate freq of (word ,tag):
    for sentence in train:
        for pair in sentence:
            if pair in word_tag_freq:
                word_tag_freq[pair] = word_tag_freq[pair] + 1
            else:
                word_tag_freq[pair] = 1

    #count unique amoutn fo tag for word
    unique_tag_per_word = {}
    for pair in word_tag_freq:
        if pair[1] in unique_tag_per_word:
            unique_tag_per_word[pair[1]] += 1
        else:
            unique_tag_per_word[pair[1]] = 1

    # calculate word_all_tag_prob
    # will contain the prob of {(word, tag) : prob}
    word_all_tag_prob = {}
    for sentence in train:
        # {(word : tag) : prob} use highest prob of word:tag to assign emission
        for pair in sentence:
            word = pair[0]
            tag = pair[1]
            count_word_pair = word_tag_freq[pair]
            pair_prob = (count_word_pair + alpha) / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
            word_all_tag_prob[pair] = math.log(pair_prob)


    emission_prob = word_all_tag_prob

    # calculating emission_prob
    # for pair in word_all_tag_prob:
    #     word = pair[0]
    #     tag = pair[1]
    #     prob = word_all_tag_prob[pair]
    #
    #     if word not in emission_prob:
    #         emission_prob[word] = tag
    #     else:
    #         #compare prob see if needs to be updated
    #         emission_tag = emission_prob[word]
    #         temp_pair = (word, emission_tag)
    #         if (prob > word_all_tag_prob[temp_pair]):
    #             emission_prob[word] = tag

    tags = []
    for sentence in train:
        for pair in sentence:
            if pair[1] not in tags:
                tags.append(pair[1])
    num_unique_tags = len(tags)


    first_iter = True
    answer = []
    counter = 0
    for sentence in test:
        first_iter = True
        word_tag_to_add = []
        for word in sentence:
            tag_holder = []
            tag_in_order = []
            for tag in tags:
                if (word, tag) not in emission_prob:
                        test = (0 + alpha) / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
                        emission_prob[(word, tag)] = -1000
                if (first_iter):
                    current_prob = init_prob + emission_prob[(word, tag)]
                    tag_holder.append(current_prob)
                    tag_in_order.append(tag)
                else:
                    #else case
                    # if (word, tag) not in emission_prob:
                    #     test = (word_freq[word] + alpha) / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
                    #     emission_prob[(word, tag)] = -1000
                    if (best_tag, tag) not in transition_prob:
                        test = (0 + alpha) / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
                        transition_prob[(best_tag, tag)] = -1000000000
                    current_prob = v + emission_prob[(word, tag)] + transition_prob[(best_tag, tag)]
                    tag_holder.append(current_prob)
                    tag_in_order.append(tag)
            v_idx = np.argmax(tag_holder)
            v = tag_holder[v_idx]
            best_tag = tag_in_order[v_idx]
            word_tag_to_add.append((word, best_tag))
            first_iter = False
        answer.append(word_tag_to_add)

    return answer
