import os
import requests
import json
import glob
import urllib
from kraken_etl.helpers import etl_io
import asyncio
from kraken_local_db.kraken_local_db import Kraken_local_db


max_no_active_tasks = 50

def load_to_db(source_path, destination_db_path, table=None):
    return asyncio.run(load_to_db_async(source_path, destination_db_path, table))


async def load_to_db_async(source_path, destination_db_path, table=None):
    """Load data into db
    """
    #todo: complete this

    db = Kraken_local_db(destination_db_path)

    files = etl_io.get_file_names(source_path)
    count = 0
    for i in files:
        records = await etl_io.load_from_json(i)
        db.post(records)
        count += 1
        print(count)
    
    return

def load_to_api(source_path, destination_url):
    """Load data to api
    """
    
    #todo: complete this

    return


def load_to_directory(source_path, destination_path):
    """Load data into target directory
    """
    return asyncio.run(load_to_directory_async(source_path, destination_path))


async def load_to_directory_async(source_path, destination_path):
    """
    """
    tasks = []
    files = etl_io.get_file_names(source_path)
    count = 0
    for i in files:

        # Task limiter. Waits if max no of active tasks achieved
        while len([x for x in tasks if x.done() is False]) > max_no_active_tasks:
            await asyncio.sleep(1)

        task = asyncio.create_task(_load_to_directory_async_step(i, destination_path, count))
        tasks.append(task)
        count += 1

    await asyncio.gather(*tasks)

    return

async def _load_to_directory_async_step(file, destination_path, count):
    """
    """
    records = await etl_io.load_from_json(file)
    await etl_io.save_records_to_file_async(records, destination_path, count)
    return
