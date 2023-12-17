import requests
import json
import asyncio
import aiohttp


async def extract_outputs(template, json_response):
    """
    Extracts data from a run_app JSON response based on a provided template.

    Args:
    - template (dict): A dictionary representing the template structure.
    - json_response (dict): The JSON response from which to extract data.

    Returns:
    - dict: A dictionary containing the extracted data.
    """
    extracted_data = {}

    # Iterate over the template to find the keys of interest
    for key in template:
        # Check if the key exists in the 'user_outputs' of the json_response
        if key in json_response.get('user_outputs', {}):
            user_output = json_response['user_outputs'][key]

            # If the 'value' is a string, return it as is
            if isinstance(user_output.get('value'), str):
                extracted_data[key] = user_output['value']
            # If the 'value' is a dictionary and contains 'arguments', return each key/value pair in 'arguments'
            elif 'arguments' in user_output.get('value', {}):
                extracted_data.update(user_output['value']['arguments'])

    return extracted_data

# Return App details
async def get_app(api_key, app_id):
    
    url = f"https://swbtw-api.onrender.com/v1/apps/{app_id}/view"
    headers = {"X-API-KEY":api_key,"Content-Type":"application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            json_response = await response.json()

    return json_response

async def get_app_templates(res_json):
    ### Todo ###
    # Add more logic with return data later
    return res_json['user_inputs'], res_json['user_outputs']


async def run_app(api_key, app_id, data_tuples_list):
    """
    Runs a Forge App and returns its user_outputs as a dictionary

    Args:
    - tuples (list of tuples): A list of tuples, where each tuple is a key/value pair.

    Returns:
    - dict: A dictionary populated with the key/value pairs gathered from get_app.
    """
    get_app_json = await get_app(api_key, app_id)
    input_template, outputs_template = await get_app_templates(get_app_json)
    data = {"user_inputs": {}}
    for key, value in data_tuples_list:
        data["user_inputs"][key] = {"value": value}

    url = f"https://swbtw-api.onrender.com/v1/apps/{app_id}/view/run?json_output=true"
    headers = {"X-API-KEY":api_key,"Content-Type":"application/json"}
     
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            json_response = await response.json()

        outputs_dict = await extract_outputs(outputs_template, json_response)

        return outputs_dict


async def run_batch(api_key, apps_tuples_list):
    """
    Runs a list of Forge App concurrently and returns 

    Args:
    - tuples (list of tuples): A list of tuples, 
    where each tuple is a app_id and a list of tupple key/value app_inputs.

    Returns:
    - list: List of user_outputs dictionaries.
    """
    tasks = []
    for app_id, app_info in apps_tuples_list:
        # Assuming you have a way to retrieve or define the api_key for each app
        tasks.append(run_app(api_key, app_id, app_info))

    results = await asyncio.gather(*tasks)
    return results

