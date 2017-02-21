from communication_objects import KeyShard
from crypto import load_key
import socket
from network_interface import send_object
import time

if __name__ == "__main__":
    # Fetch key shards(shard 1 & shard 2)
    shard_1 = load_key("../keys/shard_1.pkl")
    shard_2 = load_key("../keys/shard_2.pkl")

    # Create objects to be sent to server
    key_shard_1 = KeyShard(shard_1)
    key_shard_2 = KeyShard(shard_2)

    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", 5001))

    # Send it on port 5001(server initiation port)
    send_object(sock, key_shard_1)
    # FIX: For invalid and under constructed pickle
    # Time delay allows enough time to pickle the new object cleanly
    time.sleep(1)
    send_object(sock, key_shard_2)

    sock.close()
