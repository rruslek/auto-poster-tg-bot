import os
import time
import random
import aiohttp
import asyncio
import aiofiles
import config
import db


async def upload_image(image_num):
    async with aiohttp.ClientSession() as session:
        async with session.get('hello', proxy=None) as response:
            extension = response.headers['content-type'].split('/')[-1]
            filename = os.path.join("images", '111.txt')

            async with aiofiles.open(filename, mode='wb') as file:
                async for chunk in response.content.iter_chunked(64 * 1024):
                    await file.write(chunk)
    print(f"image: {image_num + 1} finished..")


async def generate_image(file, room_type, room_style):
    key = await db.get_sdkey()
    json_data = {
        'key': key,
        'init_image': f'https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file}',
        'prompt': f'{room_type} in {room_style} style',
        'steps': 50,
        'guidance_scale': 7
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://stablediffusionapi.com/api/v5/interior', json=json_data) as response:
            text = await response.json()
            print(text)
            if text['status'] == 'processing':
                return await fetch_image(text['id'])
            if text['status'] == 'error' and 'Your monthly limit exceeded' in text['message']:
                await db.delete_sdkey(key)
                return await generate_image(file, room_type, room_style)
            else:
                return text['output'][0]


async def fetch_image(id):
    json_data = {
        'key': 'QgkZvuJTHf7rniYsqzt7U8172tfzXe7gmO7QjvJPJ8gzYNzWskp1jGmrSwHF',
        'request_id': id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://stablediffusionapi.com/api/v4/dreambooth/fetch', json=json_data) as response:
            text = await response.json()
            return text['output'][0]
