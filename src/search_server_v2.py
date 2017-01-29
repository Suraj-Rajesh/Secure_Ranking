from generate_index import load_index
from do_parser import stem_text
import operator
from network_interface import send_object, receive_object
from communication_objects import Server_Response
import threading
import socket
from time import time

# For now, the server can serve around 170 ranked results at once for one search term
class Search_Server(object):

    def __init__(self, port = 5001, is_cached = False):
        self.port = port
        self.cached = is_cached

        # Load search index
        self.index = load_index("../index/plain_index.pkl")

        # Initialize server socket to handle incoming connections
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSock.bind(("0.0.0.0", self.port))
        self.serverSock.listen(128)

    def start(self):
        # Start listeing for incoming requests
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

        # Process query
        stemmed_query = stem_text(query)
        query_terms = list(set(stemmed_query.split()))

        # Ranked results will be stored here
        sort_index = dict()

        # Main logic for fetching ranked results from plain index here
        for keyword in query_terms:
            if keyword in self.index:
                keyword_search_index = self.index[keyword]
                for filename, value in keyword_search_index.iteritems():
                    if filename in sort_index:
                        sort_index[filename] = sort_index[filename] + value
                    else:
                        sort_index[filename] = value

        # Sort the final sort_index
        ranked_result = sorted(sort_index.items(), key=operator.itemgetter(1), reverse=True)
        ranked_result = [result[0] for result in ranked_result]

        # Get top-k results
        if top_k == 0 and len(ranked_result) > 170:
            ranked_result = ranked_result[:170]
        else:
            ranked_result = ranked_result[:top_k]

        # Note end time
        end_time = time()

        # Create response to client
        response = Server_Response(float("{0:.10f}".format(end_time - start_time)), ranked_result)

        # Send response back to the client
        send_object(server_socket, response)

        # Close socket
        server_socket.close()

if __name__ == "__main__":
    try:
        search_server = Search_Server()
        search_server.start()
    except KeyboardInterrupt:
        print "Server shutting down...\n"
