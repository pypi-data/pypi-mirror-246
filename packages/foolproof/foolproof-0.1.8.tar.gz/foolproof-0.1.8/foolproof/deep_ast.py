
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'deep_ast_c3b68b35a44d4cdd80cd739c4cc7b28c.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
