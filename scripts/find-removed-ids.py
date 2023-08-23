import subprocess

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
    for entry in git_log_delete_list:
        try:
            file_path = entry.split(' ')[4].split('/')
            # File path should have 3 entries
            if len(file_path) == 3:
                pass
            else:
                invalid_entries.append(entry)
            
        except:
            invalid_entries.append(entry)
    deleted_files = []



def convert_files_to_id(file_list):
    for file in file_list:
        print(file.split(' ')[3])

find_deleted_files(".")