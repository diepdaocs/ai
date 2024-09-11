import asyncio

import aiohttp


async def say_hello():
    print("Hello")
    await asyncio.sleep(3)
    print("World!")


async def say_goodbye():
    print("Goodbye")
    await asyncio.sleep(3)
    print("Everyone!")


async def main():
    await asyncio.gather(
        say_hello(),
        say_goodbye()
    )


# Get the event loop
loop = asyncio.get_event_loop()


# Run the coroutine
# loop.run_until_complete(main())


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch {url}: {response.status}")
            data = await response.text()
            print(f"Fetched data from {url}")
            return data
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


async def download(links):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in links]
        return await asyncio.gather(*tasks, return_exceptions=True)


urls = [
    "https://example.com/",
    "https://httpbin.org/get",
    "https://jsonplaceholder.typicode.com/posts"
]

results = loop.run_until_complete(download(urls))
# results = asyncio.run(download(urls), debug=True)

for i, result in enumerate(results):
    print(i)
    if result:
        print(f"Result {urls[i]}: {result[:100]}")
    else:
        print(f"No result from {urls[i]}")
