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



def download_from_api(source_url, destination_path):
    """
    """



def download_file(source_url, destination_path):
    """Download a file from an url and store it in destination path
    """

    # Get filename
    o = urlparse(source_url)
    path = o.path
    filename = path.split('/')[-1]
    filepath = os.path.join(destination_path, filename)

    # Create dir (if doesn't exist)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)


    # Retrieve and save file

    print(filepath)
    path, headers = urlretrieve(source_url, filepath)

    return filepath




def unzip_file(source_path, destination_path):
    """unzip a file 
    """
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    with zipfile.ZipFile(source_path,"r") as zip_ref:
        zip_ref.extractall(destination_path)

    return




def csv_to_json(source_path, destination_path, headers, delimiter):
    """
    """
    return asyncio.run(csv_to_json_async(source_path, destination_path, headers, delimiter))


async def csv_to_json_async(source_path, destination_path, headers, delimiter):
    """
    """
    tasks = []
    files = etl_io.get_file_names(source_path, '*.*')
    print(source_path, files)
    count = 0
    for i in files:

        # Task limiter. Waits if max no of active tasks achieved
        while len([x for x in tasks if x.done() is False]) > max_no_active_tasks:
            await asyncio.sleep(1)


        task = asyncio.create_task(_csv_to_json(i, destination_path, count, headers, delimiter))
        tasks.append(task)
        count += 1

    print('Waiting for tasks')
    result = await asyncio.gather(*tasks)
    print(result)

    return result

async def _csv_to_json(file, destination_path, count, headers, delimiter):
    """
    """
    print('start')
    records = await etl_io.load_from_csv(file, headers, delimiter)
    print(len(records))
    await etl_io.save_records_to_file_async(records, destination_path, count)
    return 1

