import requests
import json
import asyncio
import aiohttp
from typing import List, Optional
from functools import partial
import logging

# Forgecloud functions
from .utils import convert_data


async def extract_outputs(app_id, template, json_response):
    """
    Extracts data from a run_app JSON response based on a provided template and includes the app_id, along with template metadata.

    Args:
    - app_id (str): The ID of the Forge App from which the outputs are being extracted.
    - template (dict): A dictionary representing the template structure for outputs.
    - json_response (dict): The JSON response from which to extract data.

    Returns:
    - dict: A dictionary containing the extracted data, including the app_id and template metadata.
    """
    extracted_data = {"app_id": app_id}

    try:
        for key, template_info in template.items():
            for output_key, output_value in json_response.get('user_outputs', {}).items():
                if 'arguments' in output_value.get('value', {}):
                    if key in output_value['value']['arguments']:
                        extracted_value = output_value['value']['arguments'][key]
                        output_data = {
                            'value': extracted_value,
                            'data_type': template_info.get('data_type', 'unknown'),
                            'is_optional': template_info.get('is_optional', False)
                        }
                        extracted_data[key] = output_data
                        break
                else:
                    # Directly use the value if 'arguments' is not present
                    extracted_value = output_value.get('value')
                    output_data = {
                        'value': extracted_value,
                        'data_type': template_info.get('data_type', 'unknown'),
                        'is_optional': template_info.get('is_optional', False)
                    }
                    extracted_data[key] = output_data
    except KeyError as e:
        logging.error(f"Key error occurred while extracting outputs for app_id {app_id}: {e}")
    except TypeError as e:
        logging.error(f"Type error occurred while extracting outputs for app_id {app_id}: {e}")
    # Add other specific exceptions as needed

    return extracted_data


async def structure_results(results_list, output_structure):
    """
    Transforms a list of results from multiple run_app calls into a new dictionary
    based on the provided output structure, including error management and logging.
    Extracts a value if present in at least one of the dictionaries in results_list.

    Args:
    - results_list (list of dicts): A list containing dictionaries with the outputs of run_app calls.
    - output_structure (dict): A dictionary specifying the structure of the output.

    Returns:
    - dict: A new dictionary with data transformed according to the output structure, or None if a required key is missing.
    """
    transformed_data = {}

    for output_key, params in output_structure.items():
        print(f"output_key: {output_key}, params {params} Loop\n")
        result_key = params.get('result_key')
        app_id = params.get('app_id', None)
        conversion = params.get('conversion', None)
        is_optional = params.get('is_optional', False)

        found = False
        for result in results_list:
            print(f"result Loop: {result}\n")
            if (app_id is None or result.get('app_id') == app_id) and result_key in result:
                entry = result[result_key]
                if 'value' in entry:
                    try:
                        value = entry['value']
                        if conversion:
                            from_type, to_type = conversion
                            value = convert_data(value, from_type, to_type)
                        transformed_data[output_key] = value
                        found = True
                    except Exception as e:
                        logging.error(f"Error in conversion for key '{output_key}': {e}")
                elif not is_optional and output_key not in transformed_data:
                    logging.warning(f"Required key '{result_key}' missing in results for '{output_key}'.")

        if not found and not is_optional and output_key not in transformed_data:
            logging.warning(f"Required key '{result_key}' not found in any results for '{output_key}'.")
            return None

    return transformed_data
