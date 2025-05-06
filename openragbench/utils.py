import os
import json
import yaml


def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def write_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)


def read_jsonl(path):
    with open(path, 'r') as f:
        return [json.loads(line) for line in f]


def write_jsonl(data, path):
    with open(path, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')


def read_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def read_config(config_name):
    project_root = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(project_root, 'configs', config_name)
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
