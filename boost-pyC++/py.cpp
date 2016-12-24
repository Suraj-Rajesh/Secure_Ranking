#include <boost/python.hpp>

// To compile: g++ py.cpp -I/home/suraj/boost/include
// /home/suraj/boost/lib/libboost_python.a -lpython2.7

int main(int, char **) {
  Py_Initialize();
  PyRun_SimpleString("import hello"); 
  PyRun_SimpleString("hello.hello()"); 
  Py_Finalize();
  return 0;
}
