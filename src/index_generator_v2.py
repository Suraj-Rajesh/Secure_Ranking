from multiprocessing import Pool, Manager, Value, Lock
from crypto import load_keys, load_bcrypt_salt, load_aes_key, aes_encrypt, aes_decrypt, generate_aes_key, generate_paillier_keys
from paillier.paillier import *
from tf_idf_generator import tf, n_containing, idf, tfidf
from textblob import TextBlob as tb
from time import sleep
from os import listdir
from do_parser import doc_to_text
import cPickle as pickle
from datetime import datetime
import random
from uuid import uuid4
from hashlib import sha256

class Counter(object):
    def __init__(self, initval=0):
        self.val = Value('i', initval)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value

manager = Manager()
index = manager.dict()
encrypted_index = manager.dict()
in_use_list = manager.list()
# 0: Paillier private key, 1: Paillier public key, 2: bCrypt salt, 3: AES key
crypto_keys = manager.list()
base_index_for_encrypted = manager.dict()
counter = Counter(0)
encrypted_index_counter = Counter(0)
masking_value = Value('i', random.randint(50, 100))

corpus = dict()

def load_documents(directory):
    global corpus
    files = listdir(directory)
    for f in files:
        text = doc_to_text(directory + "/" + f)    
        textblob = tb(text)
        corpus[f] = textblob

def indexer(filename):
        global index
        global in_use_list
        global counter

	counter.increment()
	print counter.value()
        textblob = corpus[filename]
        word_score_index = {word: tfidf(word, textblob, corpus) for word in corpus[filename].words}
        for word in word_score_index:
            while word in in_use_list:
                sleep(1)
            in_use_list.append(word)
            try:
                new_value = index[word]
                new_value.update({filename:word_score_index[word]})
                index[word] = new_value
            except KeyError:
                index[word] = {filename:word_score_index[word]}
            while word in in_use_list:
                try:
                    in_use_list.remove(word)
                except ValueError:
                    pass

def save_index(filename, index):
    with open(filename, "wb") as output:
        pickle.dump(dict(index), output, -1)

def save_object(filename, obj):
    with open(filename, "wb") as output:
        pickle.dump(obj, output, -1)

def load_index(index_file):
    with open(index_file, "rb") as inpt:
        loaded_index = pickle.load(inpt)
    return loaded_index

def log_message(logfile, message):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    to_log = message + start_time + "\n"
    log_file = open(logfile, "a")
    log_file.write(to_log)
    log_file.close()

def generate_plain_index_driver(no_of_processes = 10):
    global corpus
    global index
    log_message("../logs/index_log", "Loading documents started at: ")
    load_documents("../document_corpus/prepared_documents")
    log_message("../logs/index_log", "Loading documents done, Indexing started at: ")
    pool = Pool(processes = no_of_processes)
    pool.map(indexer, corpus)
    save_index("../index/plain_index.pkl", index) 
    log_message("../logs/index_log", "Indexing ended at: ")

# Encrypted index generation functions

def encrypted_indexer(keyword):
    global encrypted_index_counter
    global encrypted_index
    global masking_value
    global base_index_for_encrypted
    global crypto_keys
    global encrypted_index_counter

    encrypted_index_counter.increment()
    print "Processing " + str(encrypted_index_counter.value()) + " of " + str(len(base_index_for_encrypted)) + "..."

    encrypted_metadata = dict()

    for filename, tf_idf in base_index_for_encrypted[keyword].iteritems():
        encrypted_metadata.update({aes_encrypt(filename, crypto_keys[3]):encrypt(crypto_keys[1], int(tf_idf * 100000) + masking_value.value)})
    encrypted_index[sha256(crypto_keys[2].encode() + keyword.encode()).hexdigest()] = encrypted_metadata

def generate_keys(key_directory):
    # Both creates keys and saves it in respective directory
    generate_aes_key()
    generate_paillier_keys()

    # SHA256 salt
    salt = uuid4().hex
    save_object(key_directory + "/salt.pkl", salt)

def generate_encrypted_index_driver(no_of_processes = 10):
    global crypto_keys
    global base_index_for_encrypted

    plain_index = load_index("../index/plain_index.pkl")
    base_index_for_encrypted = plain_index
    
    generate_keys("../keys")

    (paillier_private_key, paillier_public_key) = load_keys("../keys/private_key.pkl", "../keys/public_key.pkl")
    salt = load_index("../keys/salt.pkl")
    aes_key = load_aes_key("../keys/aes_key.pkl")

    crypto_keys.append(paillier_private_key)
    crypto_keys.append(paillier_public_key)
    crypto_keys.append(salt)
    crypto_keys.append(aes_key)

    log_message("../logs/index_log", "\nEncrypting index started at: ")
    pool = Pool(processes = no_of_processes)
    pool.map(encrypted_indexer, plain_index)

    save_index("../index/encrypted_index.pkl", encrypted_index)

    log_message("../logs/index_log", "\nEncrypting index ended at: ")

def test_index():
    loaded_index = load_index("../index/test_plain_index.pkl")
    print loaded_index

def test_encryption_module():
    crypto_keys = list()
    (paillier_private_key, paillier_public_key) = load_keys("../keys/private_key.pkl", "../keys/public_key.pkl")
    crypto_keys.append(paillier_private_key)
    crypto_keys.append(paillier_public_key)
    encr = encrypt(crypto_keys[1], 100)
    print encr

def test_encrypted_index():
    encrypted_index = load_index("../index/encrypted_index.pkl")
    print encrypted_index
