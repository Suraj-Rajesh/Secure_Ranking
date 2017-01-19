from do_parser import *
from collections import defaultdict
from textblob import TextBlob as tb
from tf_idf_generator import tf, n_containing, idf, tfidf
import cPickle as pickle
from paillier.paillier import *
from paillier_crypto import load_keys
import random

def load_documents(directory, corpus_textblobs):
    files = listdir(directory)
    for f in files:
        text = doc_to_text(directory + "/" + f)
        textblob = tb(text)
        corpus_textblobs[f] = textblob

def plain_index_generator(corpus_textblobs):
    plain_index = defaultdict(dict)
    # For each file to be indexed
    for filename, textblob in corpus_textblobs.iteritems():
        # Calculate score of all words in the textblob corresponding to that file
        word_score_index = {word: tfidf(word, textblob, corpus_textblobs) for word in textblob.words}
        # Index each word into the plain search index
        for word in word_score_index:
            plain_index[word][filename] = word_score_index[word]
    save_index("../index/plain_index.pkl", plain_index)

def mask_encrypt(value, offset, public_key):
    offseted = int(value * 100000) + offset
    encrypted_value = encrypt(public_key, offseted)
    return encrypted_value

def encrypted_index_generator(plain_index_file):
    (priv_key, pub_key) = load_keys("../keys/private_key.pkl", "../keys/public_key.pkl")
    plain_index = load_index(plain_index_file)
    offset = random.randint(50, 100)
    for keyword, keyword_index in plain_index.iteritems():
        for filename, tf_idf in keyword_index.iteritems():
            plain_index[keyword][filename] = mask_encrypt(tf_idf, offset, pub_key)
    save_index("../index/encrypted_index.pkl", plain_index)

def save_index(filename, index):
    with open(filename, "wb") as output:
        pickle.dump(index, output, -1)

def load_index(index_file):
    with open(index_file, "rb") as inpt:
        index = pickle.load(inpt)
    return index

def generate_plain_index_driver():
    corpus_textblobs = dict()
    load_documents("../corpus/prepared_documents", corpus_textblobs)
    plain_index_generator(corpus_textblobs)

def generate_encrypted_index_driver():
    encrypted_index_generator("../index/plain_index.pkl")
