#ifndef _CRYPTO_H_
#define _CRYPTO_H_

#include <stdio.h>
#include <stdlib.h>
#include <gmp.h>
#include "paillier.h"

paillier_ciphertext_t * paillier_encrypt(unsigned long int data, paillier_pubkey_t * public_key);

unsigned long int paillier_decrypt(paillier_ciphertext_t * ciphertext, paillier_pubkey_t * public_key, paillier_prvkey_t * private_key);

#endif
