

import asyncio
import aiofiles
import json
from aiocsv import AsyncWriter, AsyncReader, AsyncDictReader
import os
import glob
import xmltodict
import shutil

filepaths = []

def delete_temp(directory):
    
    # Remove temp files
    shutil.rmtree(directory, ignore_errors=True)
    return

def get_records_from_directory(source_path, limit=1):
    """Returns all records from directory, even if from multiple files
    """
    files = get_file_names(source_path, condition='*.json')

    for i in files:
        records = asyncio.run(load_from_json(i))
        offset = 0 
        flag = True

        while flag:
            if len(records) <= limit + offset:
                limit = len(records) - offset
                flag = False
            yield records[offset:limit+offset]
            offset += limit

    return



def get_file_names(source_path, condition='*.json'):
    """
    """

    filepath = os.path.join(source_path, condition)

    files = glob.glob(filepath)

    return files





async def load_from_json(filepath):
    # Read
    async with aiofiles.open(filepath, mode='r', encoding="utf8") as f:
        content = await f.read()

    records = json.loads(content)
    return records


async def load_from_csv(filepath, headers, delimiter):
    """
    """
    # dict reading, tab-separated
    records = []
    
    try:
        async with aiofiles.open(filepath, mode="r", encoding="utf-8", newline="") as afp:
            async for row in AsyncDictReader(afp, headers, delimiter=delimiter):
                records.append(row)
    
    except Exception as e:
        print(40 * '-')
        print('error', e)
        print('Trying without utf-8')
        print(40 * '-')
        async with aiofiles.open(filepath, mode="r", encoding='cp1252') as afp:
            async for row in AsyncDictReader(afp, headers, delimiter=delimiter):
                records.append(row)
    
    return records

async def load_from_xml(filepath):
    """
    """
    # dict reading, tab-separated
    records = []
    async with aiofiles.open(filepath, mode="r", encoding="utf-8", newline="") as f:
        content = await f.read()

    data_dict = xmltodict.parse(content)
    records = dict(data_dict)
    return records


def save_records_to_file(records, destination_path, count=0):
    return asyncio.run(save_records_to_file_async(records, destination_path, count))


async def save_records_to_file_async(records, destination_path, count=0):
    # Write

    global filepaths
    if destination_path not in filepaths:
        filepath = os.path.join(destination_path, 'test.txt')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        filepaths.append(destination_path)


    offset=0
    limit = 1000
    tasks = []
    count2 = 0
    flag = True

    while flag:

        if offset + limit >= len(records):
            flag = False
            limit = len(records) - offset

        filename = f'data_{str(count)}_{str(count2)}.json'
        filepath = os.path.join(destination_path, filename)    
        content = json.dumps(records[offset:offset+limit], default=str, indent=4)
        task = asyncio.create_task(_save(content, filepath))
        tasks.append(task)

        offset += limit
        count2 += 1

    result = await asyncio.gather(*tasks)

    return result


async def _save(content, filepath):
    """
    """
    async with aiofiles.open(filepath, mode='w', encoding="utf8") as f:
        await f.write(content)
    return

