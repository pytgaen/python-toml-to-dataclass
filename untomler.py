from typing import Dict

from genson import SchemaBuilder

map_schema_type_to_python = {
    "string": "str", "integer": "int", "number": "float", "boolean": "bool", "null": "None"
}

import tomli


def var_to_class_name(name):
    n = name.split('_')
    return ''.join(ele.capitalize() for ele in n)


def type_object(model: Dict, class_name: str = "Root"):
    attrs = []
    prop = model.get("properties", {})
    req = model.get("required", [])
    for name, info in prop.items():
        typ = info.get('type')
        if typ == "object":
            new_class_name = var_to_class_name(name)
            attrs.append(type_nullable(name, req, new_class_name))
            type_object(info, new_class_name)
        elif typ == "array":
            attrs.append(type_attr(name, req, info.get('items'), "array"))
        else:
            attrs.append(type_attr(name, req, {'type': typ}))

    print(f"@dataclass\nclass {class_name}:")
    for a in attrs:
        print(f"  {a}")
    print("")

    return class_name


a: None = 4


def type_attr(name, req, typ, type_type=None):
    if 'anyOf' in typ:
        r = []
        for u_typ in typ["anyOf"]:
            r.append(type_attr(name, req, u_typ, "any"))
        return f"{name}: Union[" + ",".join(r) + "]"
    # elif isinstance(typ, dict) and "type" in typ:
    #     return type_union(name, req, typ["type"])
    elif "type" in typ and isinstance(typ["type"], list):
        return type_union(name, req, typ, type_type)
    elif "type" in typ and typ["type"] == "object":
        return type_object(typ, "element")
    else:
        return type_simple(name, req, typ, type_type)


def type_nullable(name, req, py_typ):
    if name in req:
        return (f"{name}: {py_typ}")
    else:
        return (f"{name}: Optional[{py_typ}]")


def type_simple(name, req, typ, type_type=None):
    py_typ = map_schema_type_to_python.get(typ["type"], f"Unsupported_{typ}")

    if type_type == 'any':
        return (f"{py_typ}")

    return type_nullable(name, req, py_typ)


def type_union(name, req, typs, type_type):
    # {'type': ['integer', 'string']}
    # {'anyOf': [{'type': 'integer'}, {'type': 'object', 'properties': {'attr_num': {'type': 'integer'}, 'attr_cd': {'type': 'string'}}}]}

    if "type" in typs and isinstance(typs["type"], list):
        py_typs = [map_schema_type_to_python.get(typ, f"Unsupported_{typ}") for typ in typs["type"]]

    if "None" in py_typs and len(py_typs) > 1:
        py_typs.remove("None")

    if len(py_typs) == 1:
        typs_ = py_typs[0]
    else:
        typs_ = "Union[" + ", ".join(py_typs) + "]"

    if type_type == 'any':
        return (f"{typs_}")

    if type_type == 'array':
        return (f"{name}: List[{typs_}]")

    return type_nullable(name, req, typs_)


def print_vars(level, name, req, typ):
    if name in req:
        print(f"{' ' * level}{name}: {typ}")
    else:
        print(f"{' ' * level}{name}: Optional[{typ}]")


fil = "xxx.toml"

with open(fil, "rb") as f:
    toml_dict = tomli.load(f)

builder = SchemaBuilder()
# builder.add_schema({"type": "object", "properties": {}})
builder.add_object(toml_dict)
sch = builder.to_schema()
type_object(sch)

# print("-----------")
# builder2 = SchemaBuilder()
# builder2.add_object({"hi": {"toto": "me"}})
# builder2.add_object({"hi": 5})
#
# sch = builder2.to_schema()
# print(builder2.to_json(indent=2))
# print("-----------")
