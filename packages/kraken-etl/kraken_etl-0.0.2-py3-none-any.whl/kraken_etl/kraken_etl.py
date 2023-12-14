
    
import copy
from kraken_etl.helpers import json
from kraken_etl.helpers import etl_pipeline
import os
    
class Etl:
    """
    The Vehicle object contains a lot of vehicles

    Args:
        arg1 (str): The arg is used for...
        arg2 (str): The arg is used for...
        arg3 (str): The arg is used for...

    Attributes:
        record (dict): This is where we store attributes
        json (str): Record in json format
        
    """

    def __init__(self):
        self._record = {}
        self.source_path = None
        self.source_type = None
        self.destination_path = None
        self.destination_type = None
        
        self.headers = None
        self.delimiter = None
        self.map = None
        

    def __str__(self):
        """
        """
        return str(self._record)

    
    def __repr__(self):
        """
        """
        return str(self._record)

    
    def __eq__(self, other):
        """
        """
        if type(self) != type(other):
            return False
            
        if self._record == other._record:
            return True
        return False

    def __gt__(self, other):
        """
        """
        return True

        
    def run(self):
        """
        """
        if self.source_type in ['zip', 'csv']:
            if self.destination_type == 'db':
                etl_pipeline.pipeline_file_to_db(
                    self.source_path, 
                    self.headers,
                    self.delimiter,
                    self.map,
                    self.destination_path
                )
        return True

    
    def get(self, property):
        """
        """
        return self._record.get(property, None)

    
    def load(self, value):
        """
        """
        self._record = value
        return True


    def dump(self): 
        """
        """
        return copy.deepcopy(self._record)
        

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
    def record(self):
        return self.dump()

    @record.setter
    def record(self, value):
        return self.load(value)
    
    @property
    def json(self):
        return self.get_json()

    @json.setter
    def json(self, value):
        return self.set_json(value)
        

    