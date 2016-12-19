import cPickle as pickle
from paillier.paillier import *

def keygen_save(private_key, public_key):
    save_key("private_key.pkl", private_key)
    save_key("public_key.pkl", public_key)

def save_key(filename, key):
    with open(filename, "wb") as output:
        pickle.dump(key, output, -1)

def load_keys(private_key_file, public_key_file):
    with open(private_key_file, "rb") as input:
        private_key = pickle.load(input)
    with open(public_key_file, "rb") as input:
        public_key = pickle.load(input)
    return (private_key, public_key)

# Paillier Tests
if __name__ == "__main__":
    # Generate Paillier keys
    private_key, public_key = generate_keypair(128)
    print type(private_key)
    print type(public_key)
    # Two random values
    x = encrypt(public_key, 2)
    y = encrypt(public_key, 1)
    keygen_save(private_key, public_key)
    (priv_key, pub_key) = load_keys("private_key.pkl", "public_key.pkl")
    z = e_add(pub_key, x, y)
    z_decr = decrypt(priv_key, pub_key, z)
    print z_decr
