#include <gmp.h>
#include "paillier.h"
#include <stdio.h>
#include <stdlib.h>

int 
main(void){
    paillier_pubkey_t * pub;
    paillier_prvkey_t * prv;

    /* Generate public and private keys */
    paillier_keygen(1024, &pub, &prv, paillier_get_rand_devurandom);

    /* Create paillier plaintext */
    paillier_plaintext_t * plaintext1 = NULL;
    plaintext1 = paillier_plaintext_from_str("20");

    /* Encrypt plaintext using paillier encryption */
    paillier_ciphertext_t * ciphertext1 = NULL;
    ciphertext1 = paillier_enc(ciphertext1,
                               pub,
                               plaintext1,
                               paillier_get_rand_devurandom);


    /* Create paillier plaintext */
    paillier_plaintext_t * plaintext2 = NULL;
    plaintext2 = paillier_plaintext_from_str("15");

    /* Encrypt plaintext using paillier encryption */
    paillier_ciphertext_t * ciphertext2 = NULL;
    ciphertext2 = paillier_enc(ciphertext2,
                               pub,
                               plaintext2,
                               paillier_get_rand_devurandom);


    /* Create paillier plaintext */
    paillier_plaintext_t * plaintext3 = NULL;
    plaintext3 = paillier_plaintext_from_str("50");

    /* Encrypt plaintext using paillier encryption */
    paillier_ciphertext_t * res = NULL;
    res = paillier_enc(res,
                               pub,
                               plaintext3,
                               paillier_get_rand_devurandom);

    /* Check homomorphic addition */
//    paillier_ciphertext_t * res = NULL;
//    paillier_ciphertext_t * res = (paillier_ciphertext_t *)malloc(sizeof(paillier_ciphertext_t));
    paillier_mul(pub, res, ciphertext1, ciphertext2);

    /* Decryprted text */
    paillier_plaintext_t * decrypted_data = NULL;
    decrypted_data = paillier_dec(decrypted_data,
                                  pub,
                                  prv,
                                  res);

    /* Check decrypted */
    char * decrypted_str = NULL;
    decrypted_str = paillier_plaintext_to_str(decrypted_data);

    /* Print decrypted */
    printf("\nDecrypted: %s\n", decrypted_str);

    return 0;
}
