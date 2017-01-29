import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../modules/pyssss/")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import PySSSS
import StringIO


def split_secret(secret, no_of_splits, threshold):
    secret_data = StringIO.StringIO(secret)
    outputs = list()

    for i in xrange(no_of_splits):
        outputs.append(StringIO.StringIO())

    PySSSS.encode(secret_data, outputs, threshold)

    shares = [each_output.getvalue().encode('hex') for each_output in outputs]

    return shares

def recover_secret(shares):
    shares_string_io = list()
    for i in xrange(len(shares)):
        shares_string_io.append(StringIO.StringIO())

    for i in xrange(len(shares)):
        shares_string_io[i].write(shares[i].decode('hex'))

    for i in xrange(len(shares)):
        shares_string_io[i].seek(0)

    secret = StringIO.StringIO()
    PySSSS.decode(shares_string_io, secret)
    return secret.getvalue()
