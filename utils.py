import json, pandas

BASE_DIR = './'

def saveDict(data: dict, key: str) -> None:
    with open(BASE_DIR + 'data.json', 'r') as f:
        prev_data = json.load(f)
    
    prev_data[key] = data
    with open(BASE_DIR + 'data.json', 'w') as f:
        json.dump(prev_data, f)


def getData() -> dict[str, dict]:
    with open(BASE_DIR + 'data.json', 'r') as f:
        return json.load(f)


def getDF(data: dict) -> pandas.DataFrame:
    return pandas.DataFrame.from_dict(data)