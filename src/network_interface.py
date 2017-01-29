import cPickle as pickle

def send_object(sock, obj):
    """
    Use this to send objects across dataCenters
    """
    try:    
        data = pickle.dumps(obj)
        sock.send(data)
    except Exception as details:
            print details
            return None

def receive_object(sock):
    """
    Use this to receive objects across dataCenters
    """
    try:
        data = sock.recv(4096)
        obj = pickle.loads(data)
        return obj
    except Exception as details:
        print details
	return None
