import os

# Function to parse the directory
def parse_directory(path):
    directory_contents = []
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            directory_contents.append({
                'type': 'folder',
                'name': dir_name,
                'path': dir_path
            })
        for file_name in files:
            file_path = os.path.join(root, file_name)
            directory_contents.append({
                'type': 'file',
                'name': file_name,
                'path': file_path
            })
    return directory_contents