import cPickle as pickle
from bcrypt import gensalt
from paillier.paillier import *
import base64
from Crypto.Cipher import AES
from Crypto import Random
import hashlib

AES_BS = 16

pad = lambda data: data + (AES_BS - len(data) % AES_BS) * chr(AES_BS - len(data) % AES_BS)
unpad = lambda data : data[:-ord(data[len(data)-1:])]

def generate_aes_key():
    passphrase = raw_input("Enter AES passphrase: ")
    save_directory = raw_input("Directory to save the key(relative or absolute): ")
    if save_directory[-1] != '/':
        save_directory = save_directory + "/"
    name_of_the_key = raw_input("Name of the key: ")
    aes_key = hashlib.sha256(passphrase).digest()
    save_key(save_directory + name_of_the_key, aes_key)

def aes_encrypt(plain_data, aes_key):
    plain_data = pad(plain_data)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(plain_data))

def aes_decrypt(encrypted_data, aes_key):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data[16:]))

def load_aes_key(saved_path):
    with open(saved_path, "rb") as inpt:
        return pickle.load(inpt)

def generate_paillier_keys():
    key_size = int(raw_input("Key Size: "))
    save_directory = raw_input("Directory to save the keys(relative or absolute): ")
    if save_directory[-1] != '/':
        save_directory = save_directory + "/"
    name_of_private_key = raw_input("Name of private key: ")
    name_of_public_key = raw_input("Name of public key: ")
    private_key, public_key = generate_keypair(key_size)
    save_key(save_directory + name_of_private_key, private_key)
    save_key(save_directory + name_of_public_key, public_key)

def save_key(filename, key):
    with open(filename, "wb") as output:
        pickle.dump(key, output, -1)

def load_keys(private_key_file, public_key_file):
    with open(private_key_file, "rb") as inpt:
        private_key = pickle.load(inpt)
    with open(public_key_file, "rb") as inpt:
        public_key = pickle.load(inpt)
    return (private_key, public_key)

def generate_save_bcrypt_salt(path_to_save):
    salt = gensalt()
    with open(path_to_save, "wb") as output:
        pickle.dump(salt, output, -1)

def load_bcrypt_salt(saved_path):
    with open(saved_path, "rb") as inpt:
        return pickle.load(inpt)

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
