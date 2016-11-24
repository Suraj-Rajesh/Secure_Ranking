#include "crypto.h"

paillier_ciphertext_t *
paillier_encrypt(unsigned long int data, paillier_pubkey_t * public_key){
    /* Convert to paillier plaintext */
    paillier_plaintext_t * plaintext = paillier_plaintext_from_bytes((void *)&data, 32);

    /* Encrypt */
    paillier_ciphertext_t * ciphertext = paillier_enc(ciphertext,
                                                       public_key,
                                                       plaintext,
                                                       paillier_get_rand_devurandom);

    return ciphertext;
}

unsigned long int 
paillier_decrypt(paillier_ciphertext_t * ciphertext, paillier_pubkey_t * public_key, paillier_prvkey_t * private_key){
    
    /* Decrypt to paillier plaintext */
    paillier_plaintext_t * paillier_decrypted = paillier_dec(paillier_decrypted,
                                                             public_key,
                                                             private_key,
                                                             ciphertext);


    unsigned long int * decrypted_data = (unsigned long int *)paillier_plaintext_to_bytes(32, paillier_decrypted);

    return * decrypted_data;
}
