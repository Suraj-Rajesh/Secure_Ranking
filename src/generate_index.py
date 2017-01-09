from do_parser import *
from collections import defaultdict
from textblob import TextBlob as tb
from tf_idf_generator import tf, n_containing, idf, tfidf
import cPickle as pickle

corpus_textblobs = dict()
plain_index = defaultdict(dict)

def load_documents(directory):
    files = listdir(directory)
    for f in files:
        text = doc_to_text(directory + "/" + f)
        textblob = tb(text)
        corpus_textblobs[f] = textblob

def index_generator(corpus_textblobs):
    # For each file to be indexed
    for filename, textblob in corpus_textblobs.iteritems():
        # Calculate score of all words in the textblob corresponding to that file
        word_score_index = {word: tfidf(word, textblob, corpus_textblobs) for word in textblob.words}
        # Index each word into the plain search index
        for word in word_score_index:
            plain_index[word][filename] = word_score_index[word]

def encrypted_index_generator(plain_index_file):
    plain_index = load_index(plain_index_file)
    for keyword, keyword_index in plain_index.iteritems():
        for filename, tf_idf in keyword_index.iteritems():
            plain_index[keyword][filename] = encrypt(tf_idf)

def save_index(filename, index):
    with open(filename, "wb") as output:
        pickle.dump(index, output, -1)

def load_index(index_file):
    with open(index_file, "rb") as inpt:
        index = pickle.load(inpt)
    return index

if __name__ == "__main__":
#    prepare_documents("../corpus/raw_documents", "../corpus/prepared_documents")
#    load_documents("../corpus/prepared_documents")   
#    index_generator(corpus_textblobs)
#    save_index("plain_index.pkl", plain_index)
    pl_index = load_index("plain_index.pkl")
    print pl_index["propos"]
