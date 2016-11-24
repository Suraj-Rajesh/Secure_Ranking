#include "crypto.h"

int
main(void){
    paillier_pubkey_t * public_key;
    paillier_prvkey_t * private_key;

    /* Generate public and private keys */
    paillier_keygen(1024, &public_key, &private_key, paillier_get_rand_devurandom);
 
    /* Encrypt */
    paillier_ciphertext_t * ciphertext = paillier_encrypt(10, public_key);


    /* Decrypt */
    unsigned long int decrypted = paillier_decrypt(ciphertext, public_key, private_key);
    printf("Decr: %lu\n", decrypted);
    return 0;
}
