import yaml
import pandas as pd 
from datetime import datetime

def read_yaml(file_path):
  """Reads a YAML file and returns its contents as a dictionary.

  Args:
    file_path: The path to the YAML file.

  Returns:
    A dictionary containing the YAML data.
  """

  with open(file_path, 'r') as file:
    data = yaml.safe_load(file)
  return data

def dict_to_pd(dict_content:dict) -> pd.DataFrame: 
  df = pd.DataFrame(dict_content)
  return df

def get_second(time_desc: str, 
               format:str='%H:%M:%S'):
    try:
        t_second = datetime.strptime(time_desc, format)
        t_second = t_second - datetime(1900, 1, 1)
        t_second = t_second.total_seconds()
        return t_second
    except ValueError:
        return None