# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
import math
from nltk.corpus import stopwords
"""
This is the main entry point for MP3. You should only modify code
within this file and the last two arguments of line 34 in mp3.py
and if you want-- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter=1.0, pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter --laplace (1.0 by default)
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set
    predicted_labels = []
    stop_words = ["ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out", "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than", "the", "br", "i" ,'just', 'herself', 'm', 'too', 'down', 'same', "shouldn't", 'no', 'because', "doesn't", 'ma', 't', "should've", 'ain', 'here', 'the', 'does', 'you', 'be', 've', 'y', 'mustn', 's', 'again', 'did', 'between', 'these', 'all', 'doesn', 'this', 'can', 'have', 'there', "couldn't", "needn't", "don't", 'shan', 'was', 'while', 'been', 'do', 'from', 'once', 'didn', 'its', 'for', 'is', "aren't", 'theirs', 'it', 'as', 'hadn', 'them', 'to', 'll', 'themselves', 'own', 'being', 'an', 'needn', 'in', 'your', 'yours', 'our', 'hers', 'they', 'but', 'with', 'of', "isn't", 'couldn', 'only', 'now', 'him', 'over', "you'd", 'hasn', "hadn't", "you'll", 'on', 'me', 'more', 'wasn', 'having', 'isn', "hasn't", 'itself', 'his', 'aren', 'and', 'which', 'above', "you're", 'into', 'those', 'd', 'we', 'before', 'both', "wasn't", 'she', 'few', "haven't", 'after', 'myself', 'not', 'so', 'by', 'am', 'most', 'were', 're', "it's", 'each', 'shouldn', 'out', 'than', 'some', 'her', 'are', 'against', 'through', 'when', 'such', 'haven', 'weren', 'had', 'where', 'himself', "she's", "didn't", "wouldn't", 'off', 'other', 'ours', 'then', "shan't", "won't", 'nor', 'mightn', "mustn't", 'during', 'at', 'ourselves', 'if', 'yourself', 'further', 'any', 'who', 'a', 'that', 'or', 'doing', 'o', 'below', 'why', 'wouldn', 'very', "you've", 'has', 'won', 'should', "weren't", 'whom', 'about', 'don', 'how', 'up', 'until', 'will', 'what', 'under', 'he', 'my', 'i', "that'll", 'yourselves', 'their', "mightn't"]

    posWords = {}
    negWords = {}
    # these two store every word
    totalPosWords = 0
    totalNegWords = 0
    # these two store just the word, not how much each of it shows up
    numOfPosWords = 0
    numOfNegWords = 0
    # laplace smoothing bigram_smoothing_parameter

    #creates the dictionary of frequency for wrods in pos/neg reviews on tset
    for i in range(len(train_labels)):
        if (train_labels[i] == 1):
            for j in range(len(train_set[i])):
                # if (train_set[i][j].lower() in stop_words):
                #     continue
                totalPosWords += 1
                working_word = train_set[i][j].lower()
                if (working_word in posWords):
                    posWords[working_word] = posWords[working_word] + 1
                else:
                    posWords[working_word] = 1
        else:
            for j in range(len(train_set[i])):
                # if (train_set[i][j].lower() in stop_words):
                #     continue
                totalNegWords += 1
                working_word = train_set[i][j].lower()
                if (working_word in negWords):
                    negWords[working_word] = negWords[working_word] + 1
                else:
                    negWords[working_word] = 1
    #dev set word
    numOfPosWords = len(posWords)
    numOfNegWords = len(negWords)
    # these will update as we look at each review to make more accurate
    # piazza 704
    # naive bayes 4 at bottom, laplace smoothing, prob calcuation

    for email in dev_set:
        update_pos_prior = math.log(pos_prior)
        update_neg_prior = math.log(1 - pos_prior)
        for wordc in email:
            word = wordc.lower()
            #print(word)
            countInPos = 0
            countInNeg = 0
            if (word in stop_words):
                continue
            if (word not in posWords):
                # numOfPosWords += 1
                countInPos = 0
            else:
                countInPos = posWords[word]

            if (word not in negWords):
                # numOfNegWords += 1
                countInNeg = 0
            else:
                countInNeg = negWords[word]
            # V + 1 = numOfPos/NegWords bc its already updated, no need to account for
            pos_probability = math.log((countInPos + smoothing_parameter) / (totalPosWords + (smoothing_parameter * (numOfPosWords + 1))))
            neg_probability = math.log((countInNeg + smoothing_parameter) / (totalNegWords + (smoothing_parameter * (numOfNegWords + 1))))

            update_pos_prior += pos_probability
            update_neg_prior += neg_probability

        if (update_pos_prior > update_neg_prior):
            predicted_labels.append(1)
        else:
            predicted_labels.append(0)
    print(smoothing_parameter)
    return predicted_labels

def bigramBayes(train_set, train_labels, dev_set, unigram_smoothing_parameter=1.0, bigram_smoothing_parameter=1.0, bigram_lambda=0.5,pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    unigram_smoothing_parameter - The smoothing parameter for unigram model (same as above) --laplace (1.0 by default)
    bigram_smoothing_parameter - The smoothing parameter for bigram model (1.0 by default)
    bigram_lambda - Determines what fraction of your prediction is from the bigram model and what fraction is from the unigram model. Default is 0.5
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set using a bigram model
    
    return []
