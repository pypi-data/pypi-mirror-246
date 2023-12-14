
import asyncio
import aiohttp
import json


max_no_active_tasks = 20

def get(url, params):
    """
    """

    try: 
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()

    records = asyncio.run(get_async(url, params))
    
    return records
    

def post(url, records):
    """
    """

    try: 
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()

    records = asyncio.run(post_async(url, records))

    return records



async def get_async(url, params):
    """
    """

    print('Start')
    tasks = []

    limit = params.get('limit', 100)
    offset = params.get('offset', 0)
    flag = True
    
    while flag:

        # Task limiter. Waits if max no of active tasks achieved
        while len([x for x in tasks if x.done() is False]) > max_no_active_tasks:
            await asyncio.sleep(1)
        
        task = asyncio.create_task(_get_item_async(url, params))
        tasks.append(task)

        # Change flag if result is empty
        for i in tasks:
            if i.done() and len(i.result()) == 0:
                flag = False

        completed = len([x for x in tasks if x.done()])
        print('completed', completed)

    records = asyncio.gather(*tasks)
    return records


async def _get_item_async(url, params):
    """
    """

    headers = {'content-type': "application/json"}

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as response:
                content = await response.text()
                status =  response.status

    except Exception as e:
        print(e)
        return False

    if status == 200:
        records = json.loads(content)
        return records
        
    else:
        return False
        

async def post_async(url, records, limit=100):
    """
    """

    print('Start')
    tasks = []

    flag = True
    offset = 0
    
    while flag:

        # Task limiter. Waits if max no of active tasks achieved
        while len([x for x in tasks if x.done() is False]) > max_no_active_tasks:
            await asyncio.sleep(1)

        if limit + offset > len(records):
            limit = len(records) - offset
            flag = False

        task = asyncio.create_task(_get_item_async(url, records[limit:limit + offset]))
        tasks.append(task)
    
    records = asyncio.gather(*tasks)
    return records


async def _post_item_async(url, records):
    """
    """
    headers = {'content-type': "application/json"}
    
    data = json.dumps(records, default=str)
    
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, data=data) as response:
                content = await response.text()
                status =  response.status

    except Exception as e:
        print(e)
        return False

    if status == 200:
        records = json.loads(content)
        return records

    else:
        return False
