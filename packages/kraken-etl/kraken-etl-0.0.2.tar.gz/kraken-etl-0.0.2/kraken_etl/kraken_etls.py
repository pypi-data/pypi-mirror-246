
    
import copy
from kraken_etl.helpers import json
import os
from kraken_etl.kraken_etl import Etl
    
class Etls:
    """
    Collection contains many objects

    Args:
        arg1 (str): The arg is used for...
        arg2 (str): The arg is used for...
        arg3 (str): The arg is used for...

    Attributes:
        record (dict): This is where we store attributes
        json (str): Record in json format
        
    """

    def __init__(self):
        self._records = []
        

    def __str__(self):
        """
        """
        return str(self._records)

    
    def __repr__(self):
        """
        """
        return str(self._records)

    def __len__(self):
        return len(self._records)
    
    def __eq__(self, other):
        """
        """
        if type(self) != type(other):
            return False
            
        if self._records == other._records:
            return True
        return False
        
    def set(self, values):
        """
        """
        values = values if isinstance(values, list) else [values]
        for i in values:
            self._records.append(i)
        return True

    
    def get(self, property):
        """
        """
        return 

    
    def load(self, values):
        """
        """
        values = values if isinstance(values, list) else [values]
        for i in values:
            o = Etl()
            o.load(i)
            self._records.append(o)

        return True


    def dump(self): 
        """
        """
        records = []
        for i in self._records:
            records.append(i.dump())
        return records
        

    def set_json(self, value):
        """
        """
        record = json.loads(value)
        self.load(record)
        return True

    def get_json(self):
        """
        """
        return json.dumps(self.dump())

    @property
    def records(self):
        return self.dump()

    @records.setter
    def records(self, value):
        return self.load(value)
    
    @property
    def json(self):
        return self.get_json()

    @json.setter
    def json(self, value):
        return self.set_json(value)
        

    