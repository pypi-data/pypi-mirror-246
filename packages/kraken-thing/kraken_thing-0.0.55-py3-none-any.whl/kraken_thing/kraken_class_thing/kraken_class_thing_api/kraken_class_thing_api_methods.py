"""
Methos to interact with api
"""
import os
import asyncio
import aiohttp
import json
import requests

from kraken_thing import kraken_thing_methods as kr


def get(url, record_type, record_id):

    headers = {'content-type': "application/json", "Authorization": "bob"}
    params = {'@type': record_type, '@id': record_id}

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

def search(url, params):

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

def delete(url, record_type, record_id):
    
    headers = {'content-type': "application/json","Authorization": "bob"}
    params = {'@type': record_type, '@id': record_id}
    data = json.dumps(params)

    try:
        r = requests.delete(url, headers=headers, data=data)
        content = r.text
    except Exception as e:
        print(e)
        return False
    if r.status_code == 200:
        records = kr.json.loads(content)
        return True
    else:
        return False



async def get_async(url, record_type, record_id):
    """Given a record_type and id, retrieves record from url and return content as-is
    """
    headers = {'content-type': "application/json", "Authorization": "bob"}
    params = {'@type': record_type, '@id': record_id}

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as response:
                content = await response.text()
    except Exception as e:
        print('Error kraken_api - get ', e)
        return False

    if response.status == 200:
        records = kr.json.loads(content)
        return records
    else:
        return False



async def post_async(url, records):
    """Given content, post as-is
    """
    headers = {'content-type': "application/json","Authorization": "bob"}
    data = kr.json.dumps(records)
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, data=data) as response:
                content = await response.text()
    except Exception as e:
        print('Error kraken_api - post ', e)
        return False

    if response.status == 200:
        records = kr.json.loads(content)
        return records
    else:
        return False




async def delete_async(url, record_type, record_id):
    """Given content, post as-is
    """
    headers = {'content-type': "application/json","Authorization": "bob"}
    params = {'@type': record_type, '@id': record_id}
    data = json.dumps(params)
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.delete(url, data=data) as response:
                content = await response.text()
    except Exception as e:
        print('Error kraken_api - delete ', e)
        return False

    if response.status == 200:
        return True
    else:
        return False



