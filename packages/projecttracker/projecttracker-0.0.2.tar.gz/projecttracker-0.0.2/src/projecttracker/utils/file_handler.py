import json
import pandas as pd

def write_to_json(obj, file_name, method = 'a'):
    '''
    Writes object data into a JSON file.

    Args:
        obj: Object to be written to JSON.
        file_name (str): Name of the JSON file.
        method (str): Writing mode, default is 'a' (append).

    Returns:
        None
    '''
    with open(file_name, method) as json_file:
        json.dump(obj.__dict__, json_file)
        json_file.write('\n')

def read_from_json(file_name):
    '''
    Reads data from a JSON file.

    Args:
        file_name (str): Name of the JSON file.

    Returns:
        list: List containing the read JSON data.
    '''
    result_list = []
    try:
        with open(file_name, 'r') as json_file:
            for line in json_file:
                result_list.append(json.loads(line))
    except FileNotFoundError:
        pass  # If the file is not found, return an empty list
    return result_list

  
def delete_all_objects(file_path):
    '''
    Deletes all content from a specified file.

    Args:
        file_path (str): Path to the file to be cleared.

    Returns:
        None
    '''
    try:
        # Open the JSON file and read its content line by line
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Open the same file in write mode and clear its content
        with open(file_path, 'w') as file:
            pass  # Clear the file content

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

def write_to_json_dict(obj, file_name, method = 'a'):
    '''
    Writes dictionary data into a JSON file.

    Args:
        obj: Dictionary to be written to JSON.
        file_name (str): Name of the JSON file.
        method (str): Writing mode, default is 'a' (append).

    Returns:
        None
    '''
    with open(file_name, method) as json_file:
        json.dump(obj, json_file)
        json_file.write('\n')

def download_csv(data, file_path):
    '''
    Downloads a Pandas DataFrame as a CSV file.

    Args:
        data: Pandas DataFrame to be downloaded as CSV.
        file_path (str): Path to save the CSV file.

    Returns:
        None
    '''
    file_path = f"{file_path}/project_details.csv"
    data.to_csv(file_path, index=False)