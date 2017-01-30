from generate_index import load_index
from bcrypt import hashpw
from do_parser import stem_text
import operator
from crypto import load_keys, load_bcrypt_salt, load_aes_key, aes_decrypt
from network_interface import send_object, receive_object
from communication_objects import Server_Response
import threading
import socket
from paillier.paillier import e_add, decrypt
from time import time

class Encrypted_Search_Server(object):

    def __init__(self, port = 5000, is_cached = False):
        self.port = port
        self.cached = is_cached

        # Load keys
        self.aes_key = load_aes_key("../keys/aes_key.pkl")
        self.bcryt_salt = load_bcrypt_salt("../keys/bcrypt_salt.pkl")
        # 0: Private key, 1: Public key
        self.paillier_keys = load_keys("../keys/private_key.pkl", "../keys/public_key.pkl")

        # Load encrypted search index
        self.index = load_index("../index/encrypted_index.pkl")

        # Initialize server socket to handle incoming connections
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSock.bind(("0.0.0.0", self.port))
        self.serverSock.listen(128)

    def start(self):
        # Start listening for incoming requests
        while True:
            connection, address = self.serverSock.accept()
            threading.Thread(target=self.requestHandler, args=(connection, address)).start()

    def requestHandler(self, server_socket, address):
        # Receive query & search parameters from the client
        client_query_object = receive_object(server_socket)

        # Info
        print "Received request for: " + client_query_object.query_string

        # Start timer
        start_time = time()

        query = client_query_object.query_string
        top_k = client_query_object.top_k

        # Prepare the hashed query
        stemmed_query = stem_text(query)
        query_terms = list(set(stemmed_query.split()))
        hashed_query_terms = [hashpw(query.encode('utf-8'), self.bcryt_salt) for query in query_terms]

        # Ranked result will be stored here
        sort_index = dict()

        # Main logic for fetching ranked result from encrypted index goes here
        for keyword in hashed_query_terms:
            if keyword in self.index:
                keyword_search_index = self.index[keyword]
                for filename, value in keyword_search_index.iteritems():
                    # AES decrypt now
                    filename = aes_decrypt(filename, self.aes_key)

                    if filename in sort_index:
                        sort_index[filename] = e_add(self.paillier_keys[1], sort_index[filename], value)
                    else:
                        sort_index[filename] = value

        # Decrypt the sort index
        for filename, value in sort_index.iteritems():
            sort_index[filename] = decrypt(self.paillier_keys[0], self.paillier_keys[1], value)

        # Sort the final sort_index
        ranked_result = sorted(sort_index.items(), key=operator.itemgetter(1), reverse=True)
        ranked_result = [result[0] for result in ranked_result]

        # Get top-k results
        if top_k == 0:
            if len(ranked_result) > 170:
                ranked_result = ranked_result[:170]
        else:
            ranked_result = ranked_result[:top_k]

        # Note end time
        end_time = time()

        # Create response to client
        response = Server_Response(float("{0:.4f}".format(end_time - start_time)), ranked_result)

        # Send response back to the client
        send_object(server_socket, response)

        # Close socket
        server_socket.close()

if __name__ == "__main__":
    # Start the server
    try:
        encrypted_search_server = Encrypted_Search_Server()
        encrypted_search_server.start()
    except KeyboardInterrupt:
        print "Server shutting down...\n"
