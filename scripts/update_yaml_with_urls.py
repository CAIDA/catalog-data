import pandas as pd
from ruamel.yaml import YAML
import shutil
import os
from collections import OrderedDict
from ruamel.yaml.comments import CommentedMap

yaml = YAML()

# Load the YAML file, considering multiple documents
def load_yaml_list(filename):
    with open(filename, 'r') as file:
        return list(yaml.load_all(file))

# Save the updated YAML file
def save_yaml(filename, data):
    with open(filename, 'w') as file:
        yaml.dump_all(data, file)

# Load the spreadsheet
def load_spreadsheet(filename, sheet_name):
    df = pd.read_excel(filename, sheet_name=sheet_name, header=None)
    # Create a dictionary with titles as keys and tuples of (url, validation) as values
    return {row[0]: (row[1], row[2]) for _, row in df.iterrows()}

# Update the YAML data with URLs from the spreadsheet
def update_yaml_with_urls(yaml_data, url_dict):
    for entry in yaml_data:
        if not isinstance(entry, CommentedMap):
            entry = CommentedMap(entry)
        
        title = entry.get('TITLE')

        if title and 'URL' not in entry:
            url, validation = url_dict.get(title, (None, None))
            if validation == 'valid' and url:
                entry['URL'] = url_dict[title]
    return yaml_data

def main():
    original_yaml_path = '../data/data-papers.yaml'
    spreadsheet_path = '../data/CAIDA Candidate Data Papers Spreadsheet.xlsx'
    sheet_name = 'DataPublicationsURL'
    updated_yaml_path = '../data/updated_data.yaml'

    # Copy the original YAML file to a new location
    shutil.copyfile(original_yaml_path, updated_yaml_path)

    # Load data from the copied YAML file
    yaml_data = load_yaml_list(updated_yaml_path)
    url_dict = load_spreadsheet(spreadsheet_path, sheet_name)
    
    # Update YAML with URLs
    updated_yaml_data = update_yaml_with_urls(yaml_data, url_dict)

    # Save updated YAML data back to the copied file
    save_yaml(updated_yaml_path, updated_yaml_data)

if __name__ == "__main__":
    main()
