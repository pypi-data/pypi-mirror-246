import base64
import os


def encode_templates_to_dict(directory: str) -> dict:
    templates = {}
    for root, subdirs, files in os.walk(directory):
        for filename in files:
            absolute_path = root + "/" + filename
            relative_path = absolute_path.replace(directory + "/", "")
            value = open(absolute_path, "r").read()
            encoded_value = base64.b64encode(value.encode()).decode()
            templates[relative_path] = encoded_value
    return templates
