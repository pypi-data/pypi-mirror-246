import asyncio
import aiohttp
import json
from kraken_thing.kraken_class_thing.kraken_class_thing_actions import kraken_class_thing_actions_methods as m


class Thing_related_action:

    def __init__(self, thing):
        """
        """
        self._thing = thing

    
    def execute(self, action_name):
        """Dispatch for the actions
        """

        action = self.get(action_name)
        action['object'] = self._thing.dump()
        result = m.run_api(action, self._thing.dump())

        t2 = self._thing.new()
        t2.load(result)
        t2.api.post()
        
        print(result)
        return result
    
    def get(self, instrument_id=None):
        """Retrieves available actions for record
        Retrieve specific action if specified
        """
        actions = [self.get_scrape(), self.get_osint()]

        # Return only specific action if specified
        if instrument_id:
            for i in actions:
                instrument = i.get('instrument', {})
                if instrument.get('@id', None) == instrument_id:
                    actions = i
                
        
        return actions
    
    
    
    def get_scrape(self):
        """
        """
        record = self._thing.dump()
        record_type = self._thing.type
        record_id = self._thing.id
        
        action = {
            "@type": "action", 
            "name": "scrape", 
            "target": f"/{record_type}/{record_id}/action/578001c7-5664-4d9d-9663-17bb3336fdb1",
            "instrument": {
                "@type": "WebApp",
                "@id": "578001c7-5664-4d9d-9663-17bb3336fdb1",
                "name": "Krkn web scraper and extractor",
                "url": "https://scraper.krknapi.com"
            }
        
        }
        return action

    def get_osint(self):
        """
        """
        record = self._thing.dump()
        record_type = self._thing.type
        record_id = self._thing.id
    
        action = {
            "@type": "action", 
            "name": "Krkn OSINT social media accounts", 
            "target": f"/{record_type}/{record_id}/action/6f4981ed-1197-41d7-ac6d-f52c98d30b04",
            "instrument": {
                "@type": "WebApp",
                "@id": "6f4981ed-1197-41d7-ac6d-f52c98d30b04",
                "name": "scraper",
                "url": "https://osint.krknapi.com"
            }
    
        }
        return action