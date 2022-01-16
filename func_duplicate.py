import libcst as cst
from pathlib import Path
import textwrap
import xxhash
x = xxhash.xxh32()

a = cst.parse_expression("1 + 2")
print (a)

code = Path("elapsekeeper.py").read_text()
a = cst.parse_module(code)
print (a)

node_a=a.body[6]
node_a=a.body[6].body.children[4]

code_a = a.code_for_node(node_a)

x = xxhash.xxh32()
x.update(code_a)
print(code_a)
print(x.hexdigest())

de_code_a= textwrap.dedent(code_a)

x = xxhash.xxh32()
x.update(de_code_a)
print(de_code_a)
print(x.hexdigest())
