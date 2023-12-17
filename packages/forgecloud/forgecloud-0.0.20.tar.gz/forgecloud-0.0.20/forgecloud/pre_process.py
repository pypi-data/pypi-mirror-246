import requests
import json
import asyncio
import aiohttp
from typing import List, Optional
from functools import partial
import logging

from utils import convert_data
from view_app import view_app

from config import settings



async def get_app_templates(app_id):
    """
    Asynchronously retrieves application templates based on a given app_id.

    This function fetches application data using get_app, then extracts and formats user input templates 
    and output templates from the JSON response.

    Args:
    - app_id (str): The unique identifier for the application.

    Returns:
    - tuple: A tuple containing two dictionaries (user_inputs_template, user_outputs_template) 
      and the original JSON response. Returns None for each element in the tuple if an error occurs.

    Error handling includes checking for valid responses from get_app, ensuring expected data structures, 
    and handling unexpected exceptions with logging.
    """
    
    # Fetch application data
    res_json = await view_app(app_id)
    if not res_json or not isinstance(res_json, dict):
        # Log error and return None if response is invalid
        logging.error(f"Failed to get app or invalid response for app_id: {app_id}")
        return None, None, None

    # Initialize templates
    user_inputs_template = {}
    user_outputs_template = {}

    try:
        # Extract user inputs template
        user_inputs = res_json.get('user_inputs', {})
        #print(f"user_inputs: {user_inputs}")
        for key, value in user_inputs.items():
            #print(f"\n\nkey: {key}\n\nvalue: {value}\n\n")
            if isinstance(value, dict):
                user_inputs_template[key] = {
                    'type': value.get('type', 'user_input'),
                    'helper_name': value.get('helper_name', ''),
                    'is_optional': value.get('is_optional', False)
                }

        # Extract user outputs template
        user_outputs = res_json.get('user_outputs', {})
        #print(f"user_outputs: {user_outputs}")
        for key, output_info in user_outputs.items():
            # Check if 'functions_from_prompt' is present and not None
            if 'functions_from_prompt' in output_info and output_info['functions_from_prompt'] is not None:
                for function in output_info['functions_from_prompt']:
                    if isinstance(function, dict) and 'parameters' in function and 'properties' in function['parameters']:
                        for output_name, output_details in function['parameters']['properties'].items():
                            if isinstance(output_details, dict):
                                is_optional = output_name not in function['parameters'].get('required', [])
                                user_outputs_template[output_name] = {
                                    'data_type': output_details.get('type', 'unknown'),
                                    'is_optional': is_optional
                                }
            else:
                user_outputs_template[key] = {
                    'type': output_info.get('type', 'unknown'),
                    'data_type': output_info.get('type', 'String'),
                    'is_optional': not output_info.get('is_required', True)
                }
    except Exception as e:
        # Log any unexpected exceptions and return the response with None templates
        logging.error(f"Error processing templates for app_id {app_id}: {e}")
        return None, None, res_json

    return user_inputs_template, user_outputs_template, res_json

async def process_input(key: str, input_info: dict, results: List[dict], app_id: str) -> Optional[dict]:
    """
    Process and validate the input for a given key.

    Args:
    - key (str): The input key.
    - input_info (dict): The input information dictionary.
    - results (list): The list of results from previously run apps.
    - app_id (str): The app id for logging.

    Returns:
    - dict: A dictionary with processed input, or None if an error occurs.
    """
    try:
        if 'value' in input_info:
            if input_info['value'] is not None:
                return {"value": input_info['value']}
            # If value is None, try fetching from a source
            elif 'source' in input_info:
                source_info = input_info['source']
                source_app_id = source_info.get('source_app_id')
                source_output_key = source_info.get('source_output_key')

                # Fetch and process the source output
                source_output = next((result[source_output_key]['value'] for result in results if result['app_id'] == source_app_id and source_output_key in result), None)

                if source_output is None:
                    logging.error(f"Required output {source_output_key} from app {source_app_id} not found in results.")
                    return None

                conversion = source_info.get('conversion', (None, None))
                if conversion[0] and conversion[1]:
                    source_output = convert_data(source_output, *conversion)

                return {"value": source_output}

        elif results and 'source_app_id' in input_info and 'source_output_key' in input_info:
            source_app_id = input_info['source_app_id']
            source_output_key = input_info['source_output_key']

            # Fetch and process the source output from other results
            source_output = next((result[source_output_key]['value'] for result in results if result['app_id'] == source_app_id and source_output_key in result), None)

            if source_output is None:
                logging.error(f"Required output {source_output_key} from app {source_app_id} not found in results.")
                return None

            conversion = input_info.get('conversion', (None, None))
            if conversion[0] and conversion[1]:
                source_output = convert_data(source_output, *conversion)

            return {"value": source_output}

        else:
            logging.error(f"Input source for {key} is not defined correctly.")
            return None

    except Exception as e:
        logging.error(f"Error processing input {key} for app {app_id}: {e}")
        return None