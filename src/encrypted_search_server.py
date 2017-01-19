from generate_index import load_index
from do_parser import stem_text
import operator
from paillier_crypto import load_keys
from paillier.paillier import e_add, decrypt

if __name__ == "__main__":
    # Load search index
    index = load_index("../index/encrypted_index.pkl")
    (private_key, public_key) = load_keys("../keys/private_key.pkl", "../keys/public_key.pkl")

    # Start the server
    try:
        while True:
            query = raw_input("Search: ")
            stemmed_query = stem_text(query)
            query_terms = stemmed_query.split()
            sort_index = dict()

            for keyword in query_terms:
                if keyword in index:
                    keyword_search_index = index[keyword]
                    for filename, value in keyword_search_index.iteritems():
                        if filename in sort_index:
                            sort_index[filename] = e_add(public_key, sort_index[filename], value)
                        else:
                            sort_index[filename] = value

            # Decrypt the sort index
            for filename, value in sort_index.iteritems():
                sort_index[filename] = decrypt(private_key, public_key, value)
            # Sort the final sort_index
            ranked_result = sorted(sort_index.items(), key=operator.itemgetter(1), reverse=True)
            # Print for now
            for filename, value in ranked_result:
                print filename

    except Exception as details:
        print "Server shutting down..."
        print details
