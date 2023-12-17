import requests
import json
import asyncio
import aiohttp
from typing import List, Optional
from functools import partial
import logging


from utils import convert_data
from pre_process import get_app_templates, process_input
from post_process import extract_outputs, structure_results

from config import settings

async def perform_api_call_with_retry(url: str, data: dict, headers: dict, max_retries: int = 1, timeout_seconds: int = 150, retry_delay: int = 2):
    """
    Performs an API call with retry and timeout mechanisms.

    Args:
    - url (str): URL to make the API call to.
    - data (dict): Data to be sent in the API request.
    - headers (dict): Headers for the API request.
    - max_retries (int): Maximum number of retries for the API call.
    - timeout_seconds (int): Timeout in seconds for the API call.
    - retry_delay (int): Delay in seconds before retrying the API call.

    Returns:
    - dict: JSON response from the API call, or None if the call fails.
    """
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data, timeout=aiohttp.ClientTimeout(total=timeout_seconds)) as response:
                    if response.status != 200:
                        raise aiohttp.ClientError(f"HTTP error: {response.status}")
                    return await response.json()
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)  # Wait before retrying
            else:
                return None

async def run_app(app_data: dict, results: Optional[list] = None):
    """
    Runs a Forge App and returns its user_outputs as a dictionary.

    Args:
    - app_data (dict): A dictionary containing 'app_id' and 'inputs_dict'.
    - results (list of dicts, optional): A list containing dictionaries with the outputs of previously run apps. Defaults to None.
    - api_key (str): API key for authentication.

    Returns:
    - dict: A dictionary populated with the key/value pairs gathered from the app, or None if an error occurs.
    """

    try:
        # Validate app_data structure
        if not isinstance(app_data, dict) or 'app_id' not in app_data or 'inputs_dict' not in app_data:
            logging.error("app_data must be a dictionary with 'app_id' and 'inputs_dict' keys.")
            return None

        app_id = app_data['app_id']
        inputs_dict = app_data['inputs_dict']

        # Check if outputs_template is set and valid
        if 'outputs_template' not in app_data or not isinstance(app_data['outputs_template'], dict):
            try:
                # Attempt to fetch templates and configurations
                input_template, outputs_template, get_app_json = await get_app_templates(app_id)
                app_data['outputs_template'] = outputs_template
                
            except Exception as e:
                logging.error(f"Failed to fetch templates for app {app_id}: {e}")
                return None  # Or handle the error as appropriate for your use case
        else:
            outputs_template = app_data['outputs_template']

        data = {"user_inputs": {}}
        for key, input_info in inputs_dict.items():
            data["user_inputs"][key] = await process_input(key, input_info, results, app_id)

        # API call configuration
        url = f"https://swbtw-api.onrender.com/v1/apps/{app_id}/view/run?json_output=true"
        headers = {"X-API-KEY": settings.api_key, "Content-Type": "application/json"}

        # Perform API call with retry and timeout
        json_response = await perform_api_call_with_retry(url, data, headers, max_retries=1, timeout_seconds=150, retry_delay=2)
        
        if json_response is None:
            return None

        # Extract outputs
        outputs_dict = await extract_outputs(app_id, outputs_template, json_response)
        print(f'outputs_dict: {outputs_dict}')

        # Trigger actions if specified
        if 'actions' in app_data:
            for trigger, action_list in app_data['actions'].items():
                if trigger == 'on_completion':
                    for action_info in action_list:
                        action = action_info['action']
                        # Extract other options if needed
                        
                        # if asyncio.iscoroutinefunction(action):
                        #     await action(outputs_dict)  # Async action
                        # else:
                        #     action(outputs_dict)  # Sync action

        return outputs_dict

    except Exception as e:
        logging.error(f"Error in run_app for app {app_id}: {e}")
        return None