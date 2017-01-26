from multiprocessing import Pool, Manager, Value, Lock
from collections import defaultdict
from tf_idf_generator import tf, n_containing, idf, tfidf
from textblob import TextBlob as tb
from time import sleep
from os import listdir
from do_parser import doc_to_text
import cPickle as pickle
from datetime import datetime

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
in_use_list = manager.list()
counter = Counter(0)

#corpus = {"file1":tb("suraj rajesh darshan"), "file2":tb("darshan darshan"), "file3":tb("suraj rajesh")}
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

def load_index(index_file):
    with open(index_file, "rb") as inpt:
        loaded_index = pickle.load(inpt)
    return loaded_index

def log_time_message(logfile, message):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    to_log = message + start_time + "\n"
    log_file = open(logfile, "a")
    log_file.write(to_log)
    log_file.close()

def generate_plain_index_driver(no_of_processes = 10):
    global corpus
    global index
    log_time_message("../logs/index_log", "Loading documents started at: ")
    load_documents("../corpus/prepared_documents")
    log_time_message("../logs/index_log", "Loading documents done, Indexing started at: ")
    pool = Pool(processes = no_of_processes)
    pool.map(indexer, corpus)
    save_index("../index/test_plain_index.pkl", index) 
    log_time_message("../logs/index_log", "Indexing ended at: ")

def test_index():
    loaded_index = load_index("../index/test_plain_index.pkl")
    print loaded_index
