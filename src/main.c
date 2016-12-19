#include "crypto.h"

void 
write_keys_to_file(char * public_key_string, char * private_key_string){
    FILE * fp = fopen("keyfile", "w");
    fprintf(fp, "%s\n", public_key_string);
    fprintf(fp, "%s", private_key_string);
    fclose(fp);
}

void
save_ciphertext(char * ciphertext){
    FILE * fp = fopen("ciphertext", "w");
    fprintf(fp, "%s", ciphertext);
    fclose(fp);
}

int
main(void){
    paillier_pubkey_t * public_key;
    paillier_prvkey_t * private_key;

    /* Generate public and private keys */
    paillier_keygen(1024, &public_key, &private_key, paillier_get_rand_devurandom);

    /* Encrypt */
    paillier_ciphertext_t * paillier_ciphertext = paillier_encrypt(35465, public_key);
    char * out = export_paillier_ciphertext(paillier_ciphertext);
    save_ciphertext(out);
    printf("Encrypted: %s\n", out);
    printf("Size: %zu\n", strlen(out));

    /* Decrypt */
    paillier_ciphertext_t * ct = (paillier_ciphertext_t *)malloc(sizeof(paillier_ciphertext_t));
    import_paillier_ciphertext(out, ct);

    unsigned long int decrypted = paillier_decrypt(ct, public_key, private_key);
    printf("Decr: %lu\n", decrypted);

    /* Free plaintext & ciphertext */
    paillier_freeciphertext(paillier_ciphertext);
    paillier_freeciphertext(ct);

    /* Export keys to file */
    char * public_key_string = paillier_pubkey_to_hex(public_key);
    char * private_key_string = paillier_prvkey_to_hex(private_key);
    write_keys_to_file(public_key_string, private_key_string);   

    return 0;
}
