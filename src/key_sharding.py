from crypto import load_keys, save_key, convert_paillier_keys_to_secret, recover_paillier_keys_from_secret, load_key
from adi_shamir_secret_sharing import split_secret, recover_secret
from paillier.paillier import *

# 0: Private key, 1 Public key
paillier_keys = load_keys("../keys/private_key.pkl", "../keys/public_key.pkl")
paillier_secret = convert_paillier_keys_to_secret(paillier_keys[0], paillier_keys[1])

# Create shards of secret
shards = split_secret(paillier_secret, 3, 3)

# Save shards
for index in range(len(shards)):
    save_key("../keys/shard_" + str(index) + ".pkl", shards[index])

# Testing
shard_0 = load_key("../keys/shard_0.pkl")
shard_1 = load_key("../keys/shard_1.pkl")
shard_2 = load_key("../keys/shard_2.pkl")

shards = [shard_0, shard_1, shard_2]

recovered_secret = recover_secret(shards)
(priv_key, pub_key) = recover_paillier_keys_from_secret(recovered_secret)

# Testing encryption/decryption
#enc = encrypt(paillier_keys[1], 2)
#print decrypt(priv_key, pub_key, enc)
