import json
import os
import yaml


def load_test_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def get_config_value(key, default=None):
    value = os.getenv(key.upper(), default)
    return value
