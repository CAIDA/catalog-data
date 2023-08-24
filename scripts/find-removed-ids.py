import subprocess
import requests

# Find all the deleted files in the git repo
def find_deleted_files(repo_path):
    # Git log
    git_log_raw = subprocess.run(
        [   "git",
            "-C",
            repo_path,
            "log",
            "--diff-filter=D", 
            "--summary"],
        capture_output=True, text=True).stdout
    
    git_log_delete = subprocess.run(['grep', 'delete mode 100644'], 
                        input=git_log_raw, capture_output=True, 
                        text=True).stdout

    git_log_delete_list = git_log_delete.split('\n')
    invalid_entries = []
    deleted_files = []
    for entry in git_log_delete_list:
        try:
            file_path = entry.split(' ')[4].split('/')
            # File path should have 3 entries
            if len(file_path) == 3:
                if file_path[2].endswith(".json") or file_path[2].endswith(".md") or file_path[2].endswith(".MD"):
                    # Ignore all person objects
                    if file_path[1] != "person" and file_path[1] != "recipe": 
                        deleted_files.append(file_path)
            else:
                invalid_entries.append(entry)
            
        except:
            invalid_entries.append(entry)
    
    return deleted_files


# Convert file to id (e.g. software:dzdb_api)
def convert_file_to_id(file):
    return f"{file[1]}:{file[2].replace('.json', '').replace('.md', '').replace('.MD', '')}"

# Find all deleted files and return a set of all their ids
def find_deleted_files_id():
    deleted_files_id = set()
    deleted_files = find_deleted_files('.')
    for f in deleted_files:
        deleted_files_id.add(convert_file_to_id(f))
    return deleted_files_id


def get_current_ids(catalog_api_url):
    ids_current = set()
    query = """{
      search {
        edges {
           node {
              id   
           }
        }
      }
    }"""
    
    request = requests.post(catalog_api_url, json={'query': query})
    if request.status_code == 200:
        response = request.json()
        for edge in response["data"]["search"]["edges"]:
            ids_current.add(edge["node"]["id"])
    
    return ids_current

def main():
    # Get ids of all deleted files
    deleted_files_by_id = find_deleted_files_id()
    
    # Need to query CAIDA API
    current_ids = get_current_ids("https://api.catalog.caida.org/")
    deleted_not_in_catalog = deleted_files_by_id.difference(current_ids)
    print(len(deleted_not_in_catalog))


main()