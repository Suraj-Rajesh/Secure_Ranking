import cPickle as pickle
from paillier.paillier import *

def keygen_save(private_key, public_key):
    save_key("private_key.pkl", private_key)
    save_key("public_key.pkl", public_key)

def save_key(filename, key):
    with open(filename, "wb") as output:
        pickle.dump(key, output, -1)

def load_keys(private_key_file, public_key_file):
    with open(private_key_file, "rb") as inpt:
        private_key = pickle.load(inpt)
    with open(public_key_file, "rb") as inpt:
        public_key = pickle.load(inpt)
    return (private_key, public_key)

# Paillier Tests
if __name__ == "__main__":
    # Generate Paillier keys
#    private_key, public_key = generate_keypair(128)
    # Two random values
  #  x = encrypt(public_key, 2)
 #   y = encrypt(public_key, 1)
 #   keygen_save(private_key, public_key)
    (priv_key, pub_key) = load_keys("private_key.pkl", "public_key.pkl")
    x = encrypt(pub_key, 2)
    print x
    x_decr = decrypt(priv_key, pub_key, x)
 #   z = e_add(pub_key, x, y)
 #   z_decr = decrypt(priv_key, pub_key, z)
    print x_decr
