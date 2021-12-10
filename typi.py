from dataclasses import dataclass
from typing import Optional

import typic


@dataclass
class TestModel:
    id: int
    comment: str
    option: Optional[str] = ""


doc_ok_1 = {"id": 1, "comment": "hello"}
doc_ok_2 = {"id": 1, "comment": "hello", "option": "option 5G"}
doc_ko_1 = {"comment": "hello"}

protocol = typic.protocol(TestModel)
print(protocol)

t = protocol.transmute(doc_ok_1)
print(t)
t = protocol.transmute(doc_ok_2)
print(t)
try:
    t = protocol(doc_ko_1)
except TypeError as e:
    t = None
    print("--------- error ------------")
    print(e)
    print(TestModel.__annotations__)
    print(doc_ko_1)
print(t)
