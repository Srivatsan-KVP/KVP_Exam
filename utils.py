from django.forms import Form
from django.contrib.auth.models import User

import json, pandas

# BASE_DIR = './'
BASE_DIR = '/home/kvpexam/KVP_Exam/'

def parseForm(form: Form) -> tuple[bool, dict]:
    if not form.is_valid():
        return (False, { 'valid': False, 'message': 'Invalid submission!' })
    
    return (True, form.cleaned_data)

def shouldAllow(req, adminReq: bool) -> bool:
    return (User.objects.get(pk=req.user.pk).is_superuser == adminReq)


# LOGIC UTILS

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