

import copy
from kraken_ref_postalCode.helpers import json
import os
import os.path
from kraken_local_db.kraken_local_db import Kraken_local_db
from functools import lru_cache
from kraken_etl import Etl
import pkg_resources
import zipfile



@lru_cache(maxsize=32)
def get_postalCode(db_path, postal_code):

    new_db_path = pkg_resources.resource_filename('kraken_ref_postalCode', db_path)

    db = Kraken_local_db(new_db_path)
    records = db.search('address.postalCode', postal_code)
    return records


@lru_cache(maxsize=32)
def get_postalCode_by_city(db_path, city):

    new_db_path = pkg_resources.resource_filename('kraken_ref_postalCode', db_path)

    db = Kraken_local_db(new_db_path)
    records = db.search('address.addressLocality', city)
    return records


@lru_cache(maxsize=32)
def get_postalCode_by_province(db_path, province):

    new_db_path = pkg_resources.resource_filename('kraken_ref_postalCode', db_path)

    db = Kraken_local_db(new_db_path)
    records = db.search('address.addressRegion', province)
    return records


@lru_cache(maxsize=32)
def get_number_of_records(db_path):

    new_db_path = pkg_resources.resource_filename('kraken_ref_postalCode', db_path)

    db = Kraken_local_db(new_db_path)
    return len(db)



def init_db(db_path):
    """Initialize database. Unzip from archive if missing
    """
    
    new_db_path = pkg_resources.resource_filename('kraken_ref_postalCode', db_path)

    # Check if file exists
    if os.path.isfile(new_db_path):
        return True

    print('a', new_db_path)
    zip_db_path = db_path + '.zip'
    new_zip_db_path = pkg_resources.resource_filename('kraken_ref_postalCode', zip_db_path)



    # Check if zip file exists
    if not os.path.isfile(new_zip_db_path):
        print(new_zip_db_path)
        print('zip doesnt exist')
        return False


    # Unzip file
    d = pkg_resources.resource_filename('kraken_ref_postalCode', 'data')
    with zipfile.ZipFile(new_zip_db_path,"r") as zip_ref:
        zip_ref.extract('kraken_ref_postalCode.db', d)
        #zip_ref.extractall(new_db_path)

    print('d')
    
    return True
    