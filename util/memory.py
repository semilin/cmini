import os
import json
import glob
from jellyfish import damerau_levenshtein_distance as lev

from util import authors
from util.consts import JSON
from admins import ADMINS

def add(data: JSON) -> bool:
    file = f'layouts/{data["name"].lower()}.json'

    if os.path.exists(file):
        return False

    with open(file, 'w') as f:
        f.write(json.dumps(data, indent=4))

    return True

def update(data: JSON):
    file = f'layouts/{data["name"].lower()}.json'

    with open(file, 'w') as f:
        f.write(json.dumps(data, indent=4))


def remove(name: str, *, id: int, admin: bool = False) -> bool:
    file = f'layouts/{name}.json'

    if not os.path.exists(file):
        return False

    with open(file, 'r') as f:
        data = json.load(f)

    check = (data['user'] == id) or admin

    if check:
        os.remove(file)

    return check


def get(name: str) -> JSON:
    file = f'layouts/{name}.json'

    if not os.path.exists(file):
        return {}

    with open(file, 'r') as f:
        data = json.load(f)

    return data


def find(name: str) -> JSON:
    file = f'layouts/{name}.json'

    if not os.path.exists(file):
        names = [x[8:-5] for x in glob.glob(f'layouts/*.json')]
        names = sorted(names, key=lambda x: len(x))

        closest = min(names, key=lambda x: lev((''.join(y for y in x.lower() if y in name)), name))

        file = f'layouts/{closest}.json'

    with open(file, 'r') as f:
        data = json.load(f)

    return data