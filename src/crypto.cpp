#include <iostream>
#include <boost/python.hpp>

using namespace std;

long 
paillier_encrypt(int plaintext){
  Py_Initialize();
  PyRun_SimpleString("from paillier_crypto import load_keys");
  PyRun_SimpleString("from paillier.paillier import *");
  PyRun_SimpleString("(priv, pub) = load_keys(\"private_key.pkl\", \"public_key.pkl\")");
  char encrypt_str[40] = {0};
  sprintf(encrypt_str, "result = encrypt(pub, %d)", plaintext);
  sprintf(encrypt_str, "result = long(2 * %d)", plaintext);
  PyRun_SimpleString(encrypt_str);
  PyRun_SimpleString("print result");
  PyObject * module = PyImport_AddModule("__main__"); 
  assert(module);                                    
  PyObject * dictionary = PyModule_GetDict(module); 
  assert(dictionary);                              
  PyObject * result = PyDict_GetItemString(dictionary, "result");
  assert(result);                     
  assert(PyLong_Check(result));      
  unsigned long result_value = PyLong_AsLong(result);   
  cout << "Rs: " << result_value << endl;
  Py_Finalize();
  return result_value;
}
