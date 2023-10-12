#! /usr/bin/env python3

# This script will add licenses based on year of first commit to all python and readme
# files in a directory and all of its sub-directories.
# Please run the file in the catalog-data main folder. 
# i.e. you should be running the command line python scripts/add-licenses.py
# Feel free to edit the prepend and append templates, as well as the directories
# if you want to add licenses to other directores.
__author__ = "Victor Ren"
__email__ = "<victorren2002@gmail.com>"
import os
import subprocess

current_directory = os.getcwd()
root_dir = current_directory + '/sources/recipe'  # Replace with your directory path

# Feel free to alter. 
prepend_lines_py_template = [
    '# Copyright (c) {year} The Regents of the University of California',
    '# All Rights Reserved',
    ''
]

append_lines_md_template = [
    '',
    'Copyright (c) {year} The Regents of the University of California',
    'All Rights Reserved'
]

# A function to get the first commit year of a file
def get_first_commit_year(file_path):
    try:
        # Get the year of the first commit for the file
        result = subprocess.run(['git', '-C', root_dir, 'log', '--reverse', '--format=%ci', file_path], 
                                capture_output=True, text=True, check=True)
        print(file_path)
        print(result.stdout)
        year = result.stdout.split('-')[0]  # Update here, since git log returns full date (yyyy-mm-dd)
        
        return year
    except subprocess.CalledProcessError:
        return None

for dirpath, dirnames, filenames in os.walk(root_dir):
    # Skip hidden directories
    dirnames[:] = [d for d in dirnames if not d[0] == '.']
    
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)

        # Skip hidden files
        if filename.startswith('.'):
            continue

        # Extract file types
        _, ext = os.path.splitext(filename)
        
        try:
            year = get_first_commit_year(file_path)
            print(f"Year for the file {file_path} is {year}")
            if year is None:
                print(f"Could not determine first commit year for file: {file_path}")
                continue

            prepend_lines_py = [line.format(year=year) for line in prepend_lines_py_template]
            append_lines_md = [line.format(year=year) for line in append_lines_md_template]

            if ext == '.py':
                with open(file_path, 'r+') as file:
                    content = file.read()
                    file.seek(0, 0)
                    # Prepend lines to .py files
                    file.write('\n'.join(prepend_lines_py) + '\n' + content)
                
            elif ext == '.md' or ext == '.MD':
                with open(file_path, 'a') as file:
                    # Append lines to .md files
                    file.write('\n' + '\n'.join(append_lines_md))
        except:
             print(f"Could not decode file: {file_path}")