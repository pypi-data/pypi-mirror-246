from kraken_convert import convert

import os
import requests
from urllib.request import urlretrieve
import shutil
import zipfile
import requests
import csv
import json
import glob
import urllib
from urllib.parse import urlparse
from kraken_etl.helpers import etl_io

import asyncio

max_no_active_tasks = 50

def transform(source_path, destination_path, map):
    """Convert the schema of a record into another schema
    """
    return asyncio.run(transform_async(source_path, destination_path, map))


async def transform_async(source_path, destination_path, map):
    """
    """
    tasks = []
    files = etl_io.get_file_names(source_path, '*.json')
    print('convert', len(files))
    count = 0
    for i in files:

        # Task limiter. Waits if max no of active tasks achieved
        while len([x for x in tasks if x.done() is False]) > max_no_active_tasks:
            await asyncio.sleep(1)

        task = asyncio.create_task(_transform(i, destination_path, map, count))
        tasks.append(task)
        count += 1

    await asyncio.gather(*tasks)

    return

async def _transform(file, destination_path, map, count):
    """
    """
    records = await etl_io.load_from_json(file)
    mapped_records = convert(records, map)
    await etl_io.save_records_to_file_async(mapped_records, destination_path, count)
    return



