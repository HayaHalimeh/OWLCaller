
import os
import json
import hashlib
import collections
from typing import Dict, Union


def create_dir(path_to_files: str=None,
                directory: str = None):
    '''
    creates new directory and returns path to folder 
    '''
     
    to_path=os.path.join(path_to_files, directory)
    os.makedirs(to_path, exist_ok=True) 
    return to_path



def read_json_file(path_to_files: str = None):
    
    '''
    Reads a .json file 
    returns a dictionary
    '''

    with open(path_to_files, 'r') as file:
        dictionary= json.load(file)
    return dictionary


def save_json_file(out_file: Union[Dict, collections.defaultdict]=None,
                   output_path: str = None):
    
    '''
    saves to a .json file 
    '''

    with open(output_path, 'w') as out_path:
        json.dump(out_file, out_path, indent=4)




def calculate_hash(file_path: str = None):
    '''
    calculates the hash value for a file
    '''
    with open(file_path, 'rb') as file:
        data = file.read()
        return hashlib.md5(data).hexdigest()



def delete_duplicates(folder_path: str = None):

    '''
    deletes duplicates based on hash values
    '''

    hash_dict = {}

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_hash(file_path)

            if file_hash in hash_dict:
                os.remove(file_path)
            else:
                hash_dict[file_hash] = file_path



