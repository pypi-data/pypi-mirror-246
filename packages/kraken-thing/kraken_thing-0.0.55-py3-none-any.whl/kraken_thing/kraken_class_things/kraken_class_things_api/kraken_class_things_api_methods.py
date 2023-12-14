"""
Methos to interact with api
"""
import os
import asyncio
import aiohttp
import json
import requests

from kraken_thing import kraken_thing_methods as kr


def get(url, params):

    headers = {'content-type': "application/json", "Authorization": "bob"}
    
    try:
        r = requests.get(url, headers=headers, params=params)
        content = r.text
    except Exception as e:
        print(e)
        return False

    if r.status_code == 200:
        records = kr.json.loads(content)
        return records
    else:
        return False


def post(url, records):

    headers = {'content-type': "application/json","Authorization": "bob"}
    data = kr.json.dumps(records)

    try:
        r = requests.post(url, headers=headers, data=data)
        content = r.text
    except Exception as e:
        print(e)
        return False
    if r.status_code == 200:
        records = kr.json.loads(content)
        return records
    else:
        return False

def delete(url, params):

    headers = {'content-type': "application/json","Authorization": "bob"}
    data = kr.json.dumps(params)

    try:
        r = requests.delete(url, headers=headers, data=data)
        content = r.text
    except Exception as e:
        print(e)
        return False
    if r.status_code == 200:
        records = kr.json.loads(content)
        return records
    else:
        return False




def get_sameAs(url, record):
    """
    """

    record_type = record.get('@type', None)
    rules = kr.identifiers.get(record_type)

    results = []
    for rule in rules:
        params = {}
        skip = False
        for k in rule.get('keys', []):
            value = record.get(k, None)
            if not value:
                skip = True
            params[k] = value

        result = get(url, params)
        result = result if isinstance(result, list) else [result]
        results += result     

    return results
        


