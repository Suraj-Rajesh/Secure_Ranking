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
    int data1 = 15;
    paillier_plaintext_t * plaintext1 = NULL;
    plaintext1 = paillier_plaintext_from_bytes((void *)&data1, 32);

    /* Encrypt plaintext using paillier encryption */
    paillier_ciphertext_t * ciphertext1 = NULL;
    ciphertext1 = paillier_enc(ciphertext1,
                               pub,
                               plaintext1,
                               paillier_get_rand_devurandom);

    /* Create paillier plaintext */
    int data2 = 1;
    paillier_plaintext_t * plaintext2 = NULL;
    plaintext2 = paillier_plaintext_from_bytes((void *)&data2, 32);

    /* Encrypt plaintext using paillier encryption */
    paillier_ciphertext_t * ciphertext2 = NULL;
    ciphertext2 = paillier_enc(ciphertext2,
                               pub,
                               plaintext2,
                               paillier_get_rand_devurandom);
  
    /* Allocate memory for result*/
    paillier_ciphertext_t * result = (paillier_ciphertext_t *)malloc(sizeof(paillier_ciphertext_t));
    mpz_init(result->c);

    paillier_mul(pub, result, ciphertext1, ciphertext2);

    /* Decryprted text */
    paillier_plaintext_t * decrypted_data = NULL;
    decrypted_data = paillier_dec(decrypted_data,
                                  pub,
                                  prv,
                                  result);

    /* Check decrypted */
    int * decrypted_int = NULL;
    decrypted_int = (int *)paillier_plaintext_to_bytes(32, decrypted_data);

    /* Print decrypted */
    printf("Decrypted: %d\n", *decrypted_int);

    return 0;
}
