
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'deep_ast_22b5b4b6cf014f2baebeec260c89f234.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
