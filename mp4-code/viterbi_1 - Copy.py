import math
import numpy as np
"""
Part 2: This is the simplest version of viterbi that doesn't do anything special for unseen words
but it should do better than the baseline at words with multiple tags (because now you're using context
to predict the tag).
"""

def viterbi_1(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    # alpha is smoothing parameter
    alpha = 0.000001
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
                #initization of first col
                if (word_idx == 0) and (tag_idx == 0):
                    v[word_idx][tag_idx] = 0
                    continue
                if word_idx == 0:
                    v[word_idx][tag_idx] = -999999999999
                else:
                    internal_counter = 0
                    curr_max_prob = -999999999999
                    curr_best_tag = ""
                    for prev_tag in tags:

                        if (word, tag) not in emission_prob:
                            prob = (0 + alpha) / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
                            emission_prob[(word,tag)] = math.log(prob)

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
        #backtrace
        ret_sentence = []
        col_index_to_use = 0

        max = -999999999999
        for i in range(cols):
            if v[rows - 1][i] > max:
                max = v[rows - 1][i]
                col_index_to_use = i

        for i in range(rows):
            if i == 0:
                ret_sentence.append(("START","START"))
                continue
            if i == (rows - 1):
                ret_sentence.append(("END","END"))
                continue

            ret_sentence.append((sentence[i], b[i][col_index_to_use]))
            # col_index_to_use = tags.index(b[i][col_index_to_use])
        answer.append(ret_sentence)
    # for sentence in train:
    #     for pair in sentence:
    #         if pair[1] not in tags:
    #             tags.append(pair[1])
    # num_unique_tags = len(tags)
    # counter = 0
    # for sentence in test:
    #     counter += 1
    #     print(counter)
    #     #set init conditions
    #     v = [{}]
    #     prev_tag = tags[0]
    #     for tag in tags:
    #         if (sentence[0], tag) not in emission_prob:
    #             test = (0 + alpha) / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
    #             emission_prob[(sentence[0],tag)] = math.log(test)
    #         initial_prob = init_prob + emission_prob[(sentence[0], tag)]
    #         v[0][tag] = (initial_prob, None)
    #
    #     # start at 1 bc we did init condition already
    #     for word_idx in range(1, len(sentence)):
    #         v.append({})
    #         for tag in tags:
    #             word = sentence[word_idx]
    #             if (tags[0], tag) not in transition_prob:
    #                 transition_prob[(tags[0], tag)] = -100000000
    #             if (tags[0] not in v[word_idx - 1]):
    #                 v[word_idx - 1][tags[0]] = (0, prev_tag)
    #             max_transition_prob = v[word_idx - 1][tags[0]][0] + transition_prob[(tags[0], tag)]
    #             prev_tag = tags[0]
    #             for old_tags in tags[1:]:
    #                 if (old_tags, tag) not in transition_prob:
    #                     transition_prob[(old_tags, tag)] = -100000000
    #                 if (old_tags not in v[word_idx - 1]):
    #                     v[word_idx - 1][old_tags] = (0, prev_tag)
    #                 curr_transition_prob = v[word_idx - 1][old_tags][0] + transition_prob[(old_tags, tag)]
    #                 if curr_transition_prob > max_transition_prob:
    #                     max_transition_prob = curr_transition_prob
    #                     prev_tag = old_tags
    #
    #                 if (word, tag) not in emission_prob:
    #                     test = (0 + alpha) / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
    #                     emission_prob[(word,tag)] = math.log(test)
    #
    #                 total_prob = max_transition_prob + emission_prob[(word,tag)]
    #             v.append({tag :  (total_prob, prev_tag)})
    #
    #         result_sentence
    #         max_curr_prob = -9999999999999
    #         best_tag = ""
    #         parent_tag = None
    #         for pair in v[-1]:
    #             if (pair[0] > max_curr_prob):
    #                 max_current_prob = pair[0]
    #                 best_tag = pair
    #
    #
    #
    #     for

    # first_iter = True
    # answer = []
    # counter = 0
    # for sentence in test:
    #     first_iter = True
    #     word_tag_to_add = []
    #     for word in sentence:
    #         tag_holder = []
    #         tag_in_order = []
    #         for tag in tags:
    #             if (word, tag) not in emission_prob:
    #                     test = (0 + alpha) / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
    #                     emission_prob[(word, tag)] = -1000
    #             if (first_iter):
    #                 current_prob = init_prob + emission_prob[(word, tag)]
    #                 tag_holder.append(current_prob)
    #                 tag_in_order.append(tag)
    #             else:
    #                 if (best_tag, tag) not in transition_prob:
    #                     test = (0 + alpha) / (tag_freq[tag] + alpha * (unique_tag_per_word[tag] + 1))
    #                     transition_prob[(best_tag, tag)] = -10000000
    #                 current_prob = v + emission_prob[(word, tag)] + transition_prob[(best_tag, tag)]
    #                 tag_holder.append(current_prob)
    #                 tag_in_order.append(tag)
    #         v_idx = np.argmax(tag_holder)
    #         v = tag_holder[v_idx]
    #         best_tag = tag_in_order[v_idx]
    #         word_tag_to_add.append((word, best_tag))
    #         first_iter = False
    #     answer.append(word_tag_to_add)



    return answer
