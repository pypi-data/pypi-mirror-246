
"""
Class ot interact with api
"""
import json
from kraken_thing.kraken_class_things.kraken_class_things_api import kraken_class_things_api_methods as m
from kraken_thing import kraken_thing_methods as kr
import os



class Things_api:

    def __init__(self, things):

        self._things = things
        self._api_url = None

    @property
    def url(self):
        self._api_url = self._api_url if self._api_url else os.environ.get("API_URL")
        return self._api_url

    @url.setter
    def url(self, value):
        os.environ["API_URL"] = value
        self._api_url = value

    
    def get(self, params):
        """Retrieve record
        """
        record = m.get(self.url, params)
        return self._things._db_load(record)


    def get_sameAs(self, record):
        """Returns all things from api that meet rules for being the same
        """
        records = []
        records = m.get_sameAs(self.url, record)
        return self._things._db_load(records)
        
    

    def get_refs(self, record_type, record_id, params = {}):
        """Returns all objects where object is used as a value
        For example, returns all actions where instrument is given WebAPI object
        """
        params['observations'] = {"$elemMatch": {"value.@type": record_type, "value.@id": record_id}}

        return self.get(params)
    
    
    def post(self):
        """Post record
        """
        record = self._things._db_dump()
        return m.post(self.url, record)

    def delete(self, params):
        """Retrieve record
        """
        
        result = m.delete(self.url, params)
        return result



    def delete_all(self):
        """Retrieve record
        """
        return m.delete(self.url, '*', '*')

