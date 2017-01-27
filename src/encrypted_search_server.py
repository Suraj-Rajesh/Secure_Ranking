from generate_index import load_index
from bcrypt import hashpw
from do_parser import stem_text
import operator
from crypto import load_keys, load_bcrypt_salt, load_aes_key, aes_decrypt
from paillier.paillier import e_add, decrypt

aes_key = load_aes_key("../keys/aes_key.pkl")

if __name__ == "__main__":
    # Load search index
    index = load_index("../index/encrypted_index.pkl")
    (private_key, public_key) = load_keys("../keys/private_key.pkl", "../keys/public_key.pkl")
    bcryt_salt = load_bcrypt_salt("../keys/bcrypt_salt.pkl")

    # Start the server
    try:
        while True:
            query = raw_input("Search: ")
            stemmed_query = stem_text(query)
            query_terms = list(set(stemmed_query.split()))
            hashed_query_terms = [hashpw(query.encode('utf-8'), bcryt_salt) for query in query_terms]
            sort_index = dict()

            for keyword in hashed_query_terms:
                if keyword in index:
                    keyword_search_index = index[keyword]
                    for filename, value in keyword_search_index.iteritems():
                        # AES decrypt now
                        filename = aes_decrypt(filename, aes_key)

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
            for filename, score in ranked_result:
                print filename

    except Exception as details:
        print "Server shutting down..."
        print details
