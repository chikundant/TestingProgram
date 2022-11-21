import json


def write(data, filename):
    data = json.dumps(data)
    data = json.loads(str(data))
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=6)


def read(filename):
    with open(filename, 'r') as file:
        return json.load(file)

