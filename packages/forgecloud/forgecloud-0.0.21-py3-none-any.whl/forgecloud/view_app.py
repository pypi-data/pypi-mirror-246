import requests
import json
import asyncio
import aiohttp
from typing import List, Optional
from functools import partial
import logging

from config import settings

async def view_app(app_id:str):
    if not app_id:
        logging.error("Invalid app_id provided.")
        return None

    url = f"https://swbtw-api.onrender.com/v1/apps/{app_id}/view"
    headers = {"X-API-KEY": settings.api_key, "Content-Type": "application/json"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status != 200:
                    logging.error(f"HTTP error occurred: {response.status}")
                    return None
                try:
                    json_response = await response.json()
                except aiohttp.ContentTypeError:
                    logging.error("Invalid response format (not JSON).")
                    return None
                return json_response
    except aiohttp.ClientError as e:
        logging.error(f"Network error occurred: {e}")
    except asyncio.TimeoutError:
        logging.error("Request timed out.")
    return None
