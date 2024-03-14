import base64
from graphql import parse


def read_and_encode_type_definitions(type_definitions: str):
    try:
        type_definitions_file = open(type_definitions)
    except FileNotFoundError:
        print("Could not open provided type definitions as file, trying as GraphQL SDL")
    else:
        type_definitions = type_definitions_file.read()

    parse(type_definitions)

    return base64.b64encode(type_definitions.encode()).decode()
