from os import listdir
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

cached_stopwords = stopwords.words("english")

# Process text, extract and tokenize words
def tokenize(text):
    try:
        tokenizer = RegexpTokenizer(r'\w+')
        tokenized_text = " ".join(tokenizer.tokenize(text))
        return tokenized_text.lower()
    except Exception as details:
        print "Exception in: do_parser.tokenize()"
        print details

# Remove stopwords from text
def stopwords_remover(text):
    try:
        # Remove unicode from text
        text.decode('unicode_escape').encode('ascii','ignore')
        parsed_text = ' '.join([word for word in text.split() if word not in cached_stopwords])
        return parsed_text
    except Exception as details:
        print "Exception in: do_parser.stopwords_remover()"
        print details

# Text to document
def text_to_doc(text, document):
    try:
        with open(document, "w") as file_to_write:
            file_to_write.write(text)
    except Exception as details:
        print "Exception in: do_parser.text_to_doc()"
        print details

# Document to text
def doc_to_text(document):
    try:
        with open(document, "r") as file_to_read:
            text =file_to_read.read()
        return text
    except Exception as details:
        print "Exception in: do_parser.doc_to_text()"
        print details

# Process raw documents
def prepare_documents(source_directory, destination_directory):
    try:
        files = listdir(source_directory)
        for f in files:
            raw_text = doc_to_text(source_directory + "/" + f)
            tokenized_text = tokenize(raw_text)
            processed_text = stopwords_remover(tokenized_text)
            text_to_doc(processed_text, destination_directory + "/" + f)
    except Exception as details:
        print "Exception in: do_parser.prepare_documents()"
        print details
