# Secure_Ranking
Top-k ranking on encrypted data in the cloud

# Dependencies:

# Paillier semi-homomorphic encryption:

1. Paillier encryption scheme implemented using Python 'paillier' module.

   github: https://github.com/mikeivanov/paillier

   'paillier' is located in 'modules'

2. 'libpaillier', C library to implement Paillier key generation,
   encryption, decryption and homomorphic properties of Paillier encryption
   scheme. 

   github: https://github.com/tradams/alice-bob-sip/tree/master/libs/libpaillier-0.8

   'libpaillier' installation instructions:

   1. Download the .tar.gz package from http://acsc.cs.utexas.edu/libpaillier/
   2. Extract and follow the instructions in INSTALL file in libpaillier
      directory to install the library.
   3. Library usage is documented in paillier.h 

3. 'libpaillier' uses 'GNU Multiple Precision Arithmetic Library' (GMP) to
   perform underlying mathematial computations. So, in order to use
   libpaillier, GMP library needs to be installed first. 

   1. Instructions to install GMP library in Ubuntu is detailed clearly in this 
      blogpost, http://linkevin.me/tutorial-installing-gmp-library-ubuntu/

Once both are installed, to use 'libpaillier', first #include <gmp.h> before
including paillier.h

Compiling:

gcc main.c -lpaillier -lgmp -L<path to libpaillier>

# Order Preserving Encryption:

Symmetric order preserving encryption is utilized using python
'pyope'(Boldyreva's paper on Order Preserving Encryption). 

URL: https://pypi.python.org/pypi/pyope/

'pyope-0.0.2' directory in 'modules' contains the python module.

# NOTE: Edit the bashrc file to configure PYTHONPATH

Add this in your .bashrc,

export PYTHONPATH="${PYTHONPATH}:/home/username/Secure_Ranking/modules/paillier/:/home/username/Secure_Ranking/modules/pyope-0.0.2/"

export PYTHONPATH

$ source ~/.bashrc
