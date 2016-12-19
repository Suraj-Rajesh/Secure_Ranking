#include "crypto.h"

paillier_ciphertext_t * 
paillier_encrypt(unsigned long int data, paillier_pubkey_t * public_key){
    /* Convert to paillier plaintext */
    paillier_plaintext_t * plaintext = paillier_plaintext_from_bytes((void *)&data, 32);

    /* Encrypt */
    paillier_ciphertext_t * paillier_ciphertext = paillier_enc(paillier_ciphertext,
                                                       public_key,
                                                       plaintext,
                                                       paillier_get_rand_devurandom);

    return paillier_ciphertext;
}

char *
export_paillier_ciphertext(paillier_ciphertext_t * ct){
    return mpz_get_str(NULL, 10, ct->c);
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

void
import_paillier_ciphertext(char * ciphertext, paillier_ciphertext_t * paillier_ciphertext){
	mpz_init(paillier_ciphertext->c);
	mpz_set_str(paillier_ciphertext->c, ciphertext, 10);
}
