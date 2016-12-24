#ifndef _CRYPTO_H_
#define _CRYPTO_H_

#include <iostream>
#include <boost/python.hpp>

long
paillier_encrypt(int plaintext);

int
paillier_decrypt(long ciphertext);

#endif
