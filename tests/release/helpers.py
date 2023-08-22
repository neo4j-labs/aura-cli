import json
from jsonschema import validate, ValidationError


def validate_json_output(output, schema, is_json=False):
    try:
        data = output
        if not is_json:
            data = json.loads(output)

        with open(f"./schemas/{schema}", "r") as f:
            schema = json.load(f)

        validate(instance=data, schema=schema)
    except json.JSONDecodeError:
        raise Exception("Failed to decode JSON output.")
    except ValidationError as ve:
        raise Exception(f"JSON schema validation error: {ve.message}")

    return data
