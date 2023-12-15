
    
import copy
from kraken_ref_postalCode.helpers import json
import os
from kraken_local_db.kraken_local_db import Kraken_local_db
from functools import lru_cache
from kraken_etl import Etl
import pkg_resources

from kraken_ref_postalCode import kraken_ref_methods as m

class Ref_postalcode:
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
        
        #self._db_path = 'kraken_ref_postalCode/data/kraken_ref_postal_code.db'

        self._db_path = 'data/kraken_ref_postalCode.db'
        m.init_db(self._db_path)

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

    def __len__(self):
        return m.get_number_of_records(self._db_path)
        
    def set(self, property, value):
        """
        """
        self._record[property] = value
        return True

    

    def get(self, postal_code):
        """Returns geoCoordinates object associated with a postal code
        Use % for unknown postal codes elements
        """
        return m.get_postalCode(self._db_path, postal_code)
        

    def postalCode(self, postal_code):
        return m.get_postalCode(self._db_path, postal_code)

    def city(self, city):
        """Returns all geoCoordinates in the city
        """
        return m.get_postalCode_by_city(self._db_path, city)

    def province(self, province):
        """Returns all geoCoordinates in the province
        """
        return m.get_postalCode_by_city(self._db_path, province)

    
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
        

    def refresh(self): 

        url = 'https://download.geonames.org/export/zip/CA_full.csv.zip'


        headers = ['country_code', 'postal_code', 'place_name', 'admin_name1', 'admin_code1', 'admin_name2', 'admin_code3','admin_name4', 'admin_code4','lat', 'lon', 'accuracy']
        delimiter = '\t'

        destination_path = self.db_path

        map = {
            "@type": "geoCoordinates",
            "address":
            {
                "@type": "'address'",
                "addressLocality": "r.place_name",
                "addressRegion": "r.admin_name1",
                "addressCountry": "r.country_code",
                "postalCode": "r.postal_code",
            },
            "latitude": "r.lat",
            "longitude": "r.lon",
            "addressCountry": "r.country_code"
        }

        etl = Etl()
        etl.source_path = url
        etl.source_type = 'zip'

        etl.delimiter = delimiter
        etl.headers = headers
        etl.destination_path = destination_path
        etl.destination_type = 'db'
        etl.map = map


        etl.run()
        return