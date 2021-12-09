from typing import Dict

from genson import SchemaBuilder

map_schema_type_to_python = {
    "string": "str", "integer": "int", "number": "float", "boolean": "bool", "null": "None"
}


def var_to_class_name(name):
    n = name.split('_')
    return ''.join(ele.capitalize() for ele in n)


def generate_dataclass(model: Dict, class_name: str = "Root"):
    attrs = []
    if model["type"] == "object":
        prop = model["properties"]
        req = model.get("required", [])
        for name, info in prop.items():
            typ = info.get('type')
            if typ == "object":
                new_class_name = var_to_class_name(name)
                attrs.append(type_nullable(name, req, new_class_name))
                generate_dataclass(info, new_class_name)
            elif typ == "array":
                attrs.append(type_attr(name, req, info.get('items')))
            else:
                attrs.append(type_attr(name, req, typ))

        print(f"class {class_name}")
        for a in attrs:
            print(f"  {a}")
        print("")


a: None = 4


def type_attr(name, req, typ):
    if isinstance(typ, dict) and "type" in typ:
        return type_array(name, req, typ["type"])
    elif isinstance(typ, list):
        return type_array(name, req, typ)
    else:
        return type_simple(name, req, typ)


def type_nullable(name, req, py_typ):
    if name in req:
        return (f"{name}: {py_typ}")
    else:
        return (f"{name}: Optional[{py_typ}]")


def type_simple(name, req, typ):
    py_typ = map_schema_type_to_python.get(typ, f"Unsupported_{typ}")
    return type_nullable(name, req, py_typ)


def type_array(name, req, typs):
    # {'type': ['integer', 'string']}
    # {'anyOf': [{'type': 'integer'}, {'type': 'object', 'properties': {'attr_num': {'type': 'integer'}, 'attr_cd': {'type': 'string'}}}]}

    py_typs = [map_schema_type_to_python.get(typ, f"Unsupported_{typ}") for typ in typs]

    if "None" in py_typs and len(py_typs) > 1:
        py_typs.remove("None")

    if len(py_typs) == 1:
        typs_ = py_typs[0]
    else:
        typs_ = "Union[" + ", ".join(py_typs) + "]"

    return type_nullable(name, req, typs_)


def print_vars(level, name, req, typ):
    if name in req:
        print(f"{' ' * level}{name}: {typ}")
    else:
        print(f"{' ' * level}{name}: Optional[{typ}]")


builder = SchemaBuilder()
# builder.add_schema({"type": "object", "properties": {}})
# builder.add_object({"hi": "there"})
builder.add_object({"h_int": 5})
builder.add_object({"he_llo": {"attr_name": "toto"}})
builder.add_object({"lst_int_str": [1, "2"]})
# builder.add_object({"lst_obj": [{"attr_num": 1}, {"attr_cd": "toto"}, 5]})
builder.add_object({"h_float": 4.5})
builder.add_object({"h_str": "my"})
builder.add_object({"h_bool": True})
builder.add_object({"h_null": None})
builder.add_object({"h_any": None})
builder.add_object({"h_any": "any"})
builder.add_object({"h_any": 22})
print(builder.to_json(indent=2))
sch = builder.to_schema()
generate_dataclass(sch)

# print("-----------")
# builder2 = SchemaBuilder()
# builder2.add_object({"hi": {"toto": "me"}})
# builder2.add_object({"hi": 5})
#
# sch = builder2.to_schema()
# print(builder2.to_json(indent=2))
# print("-----------")
