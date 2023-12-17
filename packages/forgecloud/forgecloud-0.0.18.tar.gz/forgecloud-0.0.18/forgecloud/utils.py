from typing import List, Optional
from functools import partial
import logging
import json

def convert_data(source_output, from_type, to_type):
    """
    Converts data from one type to another based on the specified from_type and to_type.
    Handles a wide range of conversions.
    """
    try:
        # String Conversions
        if to_type == str:
            if from_type == List[int]:
                return ' '.join(map(str, source_output))
            elif from_type == List[str]:
                return ' '.join(source_output)
            elif from_type in [int, float, bool]:
                return str(source_output)
            elif from_type == dict:
                return json.dumps(source_output)
            elif from_type == List[dict]:
                return json.dumps(source_output)
            elif from_type == List[float]:
                return ' '.join(map(str, source_output))

        # Numeric Conversions
        elif to_type in [int, float]:
            if from_type == str:
                return to_type(source_output)
            elif from_type == List[str]:
                return list(map(to_type, source_output))
            elif from_type == List[int] and to_type == float:
                return list(map(float, source_output))

        # Boolean Conversion
        elif to_type == bool:
            if from_type == str:
                return source_output.lower() in ['true', '1', 'yes']
            elif from_type in [int, float]:
                return bool(source_output)

        # List Conversions
        elif to_type == List[str]:
            if from_type == str:
                return source_output.split()
            elif from_type == List[int]:
                return list(map(str, source_output))
            elif from_type == List[float]:
                return list(map(str, source_output))

        # Conversion from List[str] to List[int]
        elif from_type == List[str] and to_type == List[int]:
            return list(map(int, source_output))

        # JSON Conversion
        elif to_type == dict:
            if from_type == str:
                return json.loads(source_output)

    except ValueError as e:
        logging.error(f"ValueError during conversion: {e}")
        return None
    except Exception as e:
        logging.error(f"General error during conversion: {e}")
        return None
    
    logging.error(f"""\n
                  Conversion type not implemented or invalid data.\n
                  from_type: {from_type}, to_type: {to_type}\n
                  source: {source_output}\n
                  """)
    return None