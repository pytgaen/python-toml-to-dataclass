from typing import Dict

from genson import SchemaBuilder

map_schema_type_to_python = {
    "string": "str", "integer": "int"
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
                attrs.append(type_attr(name, req, new_class_name))
                generate_dataclass(info, new_class_name)
            if typ == "array":
                attrs.append(type_array(name, req, info.get('items')))
            else:
                attrs.append(type_attr(name, req, map_schema_type_to_python.get(typ, f"Unsupported_{typ}")))

        print(f"class {class_name}")
        for a in attrs:
            print(f"  {a}")
        print("")


def type_attr(name, req, typ):
    if name in req:
        return (f"{name}: {typ}")
    else:
        return (f"{name}: Optional[{typ}]")


def type_array(name, req, typs):
    py_typs = [map_schema_type_to_python.get(typ, f"Unsupported_{typ}") for typ in typs["type"]]
    if len(py_typs) == 1:
        typs_ = py_typs
    else:
        typs_ = "Union[" + ", ".join(py_typs) + "]"

    if name in req:
        return (f"{name}: {typs_}")
    else:
        return (f"{name}: Optional[{typs_}]")


def print_vars(level, name, req, typ):
    if name in req:
        print(f"{' ' * level}{name}: {typ}")
    else:
        print(f"{' ' * level}{name}: Optional[{typ}]")


builder = SchemaBuilder()
# builder.add_schema({"type": "object", "properties": {}})
# builder.add_object({"hi": "there"})
builder.add_object({"hi": 5})
builder.add_object({"he_llo": {"lv": "toto"}})
builder.add_object({"lst": [1, "2"]})
print(builder.to_json(indent=2))
sch = builder.to_schema()
generate_dataclass(sch)

print("-----------")
builder2 = SchemaBuilder()
builder2.add_object({"hi": {"toto": "me"}})
builder2.add_object({"hi": 5})

sch = builder2.to_schema()
print(builder2.to_json(indent=2))
print("-----------")
