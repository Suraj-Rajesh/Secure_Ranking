from __future__ import division, unicode_literals
import math
from textblob import TextBlob as tb
from do_parser import doc_to_text
from os import listdir

def tf(word, blob):
    return (float)(blob.words.count(word)) / (float)(len(blob.words))

def n_containing(word, bloblist):
    return (float)(sum(1 for blob in bloblist if word in blob))

def idf(word, bloblist):
    return (float)(math.log(len(bloblist)) / (float)(1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return (float)((float)(tf(word, blob)) * (float)(idf(word, bloblist)))

def generate_index(textblob):
    for blob in textblob:
        pass
        # Check if word already exists in index
        # If it exists, append details, eg: {creat: {1:0.456, 2:0.874}}
        # Else, crete a new dictionary entry with a nested dictionary, eg: {create: {1:0.456}}

#bloblist = [document1, document2, document3, document4]
#for i, blob in enumerate(bloblist):
#    print("Top words in document {}".format(i + 1))
#    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
#    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#    for word, score in sorted_words[:3]:
#        print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
