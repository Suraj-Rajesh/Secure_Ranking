#include "crypto.hpp"

using namespace std;

int 
main(){
    int no;
    cout << "Enter no: " << endl;
    cin >> no;
    long enc = paillier_encrypt(no);
    cout << enc << endl;
    return 0;
}
