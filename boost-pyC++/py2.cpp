#include <iostream>
#include <boost/python.hpp>

using namespace std;

int main(int, char **) {
  Py_Initialize();
  
  PyRun_SimpleString("result = long(5 ** 2)");
  
  PyObject * module = PyImport_AddModule("__main__"); // borrowed reference

  assert(module);                                     // __main__ should always exist
  PyObject * dictionary = PyModule_GetDict(module);   // borrowed reference
  assert(dictionary);                                 // __main__ should have a dictionary
  PyObject * result
    = PyDict_GetItemString(dictionary, "result");     // borrowed reference

  assert(result);                                     // just added result
  assert(PyLong_Check(result));                        // result should be an integer
  long result_value = PyLong_AsLong(result);          // already checked that it is an int
  
  cout << result_value << endl;
  
  Py_Finalize();
  return 0;
}
