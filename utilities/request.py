import aiohttp
import asyncio

async def get(urls):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = [_get_data(session, url) for url in urls]
            all_data = await asyncio.gather(*tasks, return_exceptions=True)
            return all_data
    except:
        raise Exception("Unable to fetch data")
        
    
async def _get_data(session, url):
    response = await session.request("GET", url=url)
    print(response)
    data = await response.json()
    return data