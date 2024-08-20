import json
import shutil
import os

# File paths
json_file_path = 'output.json'
latest_dir = 'docker/ubuntu22/rocm-6.2/'
stable_dir = 'docker/rocm/ubuntu22/6.0/'

# Ensure the directories exist
os.makedirs(latest_dir, exist_ok=True)
os.makedirs(stable_dir, exist_ok=True)

# Function to move the file based on conditions
def move_file_based_on_content(file_path):
    # Read and parse the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract the relevant values
    component = data.get('component')
    version = data.get('version')

    # Determine the target directory
    if component == 'pytorch' and version == 'latest':
        target_dir = latest_dir
    else:
        target_dir = stable_dir

    # Define the target file path
    base_name = os.path.basename(file_path)
    target_file_path = os.path.join(target_dir, base_name)

    # Move the file
    shutil.move(file_path, target_file_path)
    print(f"File moved to: {target_file_path}")

# Execute the function
move_file_based_on_content(json_file_path)
