import io

async def fetch_json(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            return None

async def fetch_img(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            image = io.BytesIO(await response.read())
            return image
        else:
            return None
