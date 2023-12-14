
"""
Class ot interact with api
"""
import json
from kraken_thing.kraken_class_thing.kraken_class_thing_api import kraken_class_thing_api_methods as m
from kraken_thing import kraken_thing_methods as kr
import os

class Thing_api:

    def __init__(self, thing):

        self._thing = thing
        self._api_url = None

    @property
    def url(self):
        self._api_url = self._api_url if self._api_url else os.environ.get("API_URL")
        return self._api_url

    @url.setter
    def url(self, value):
        os.environ["API_URL"] = value
        self._api_url = value

    def get(self):
        """Retrieve record
        """
        record = m.get(self.url, self._thing.type, self._thing.id)
        return self._thing._db_load(record)

    def post(self):
        """Post record
        """
        record = self._thing._db_dump()
        return m.post(self.url, record)
        
    def delete(self):
        """Retrieve record
        """

        result = m.delete(self.url, self._thing.type, self._thing.id)
        return result

        

    def delete_all(self):
        """Retrieve record
        """
        return m.delete(self.url, '*', '*')



    
    async def get_async(self):
        """Retrieve record
        """
        record = await m.get_async(self.url, self._thing.type, self._thing.id)
        return self._thing._db_load(record)

    async def post_async(self):
        """Post record
        """
        record = self._thing._db_dump()
        return await m.post_async(self.url, record)
    
    async def delete_async(self):
        """Retrieve record
        """
        result = await m.delete_async(self.url, self._thing.type, self._thing.id)
        return result