import json
import os
import shutil
#from urllib.parse import urlparse

# Retrieve input parameters from environment variables
schema_version = os.getenv('schema_version', 'V4')
submit_date = os.getenv('submit_date', '2024-08-16')
component_version = os.getenv('component_version', 'pytorch/12.1')
repo_commithash = os.getenv('repo_commithash', 'https://github.com/repo/pytorch/commit/r497th98r7bf87')
rocm_cuda_details = os.getenv('rocm_cuda_details', '98.44/{"comment" : "Additional details about ROCm score: string"}')
gfx_rocm = os.getenv('gfx_rocm', 'MI250/6.1')
nvarch_cuda = os.getenv('nvarch_cuda', 'A10G/12.1')
ttg_rat_rs_details = os.getenv('ttg_rat_rs_details', '359944/358763/99.67/{"comment" : "Additional details about ROCm score: string"')
cat_cs_details = os.getenv('cat_cs_details', '359149/99.77/{"comment" : "Additional details about CUDA score: string"}')
version_details = os.getenv('version_details', {"mkl" : "2024.1", "python" : "3.8"})

# Custom JSONEncoder to format without extra new lines
class CustomJSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        # Use the default encoding method
        return super().encode(obj).replace('\n ', ' ')

# Process `component_version`
component, version = component_version.split('/')

# Process `repo_commithash`
repo, commithash = repo_commithash.split('/commit/')
#parsed_url = urlparse(repo_commithash)
#repo = parsed_url.path.split('/commit/')[0]
#commit_hash = parsed_url.path.split('/commit/')[1]

# Process `rocm_cuda_details`
rocm_cuda_score, rocm_cuda_score_value = rocm_cuda_details.split('/', 1)
rocm_cuda_score_value = rocm_cuda_score_value.strip()
rocm_cuda_score_details = json.loads(rocm_cuda_score_value)

# Process `gfx_rocm`
gfxarch, rocm_version = gfx_rocm.split('/')

# Process `nvarch_cuda`
nvarch, cuda_version = nvarch_cuda.split('/')

# Process `ttg_rat_rs_details`
aisw_test_target_goal, rocm_actual_testcount, rocm_score, rocm_score_value = ttg_rat_rs_details.split('/', 3)
rocm_score_value = rocm_score_value.strip()
rocm_score_details = json.loads(rocm_score_value)

# Process `cat_cs_details`
cuda_actual_testcount, cuda_score, cuda_score_value = cat_cs_details.split('/', 2)
cuda_score_value = cuda_score_value.strip()
cuda_score_details = json.loads(cuda_score_value)

# Process `version_details`
version_details_dict = json.loads(version_details)

# Construct JSON object
output_json = {
    "schema_version": schema_version,
    "submit_date": submit_date,
    "component": component,
    "version": version,
    "repo": repo,
    "commitHash": commithash,
    "aisw_test_target_goal": aisw_test_target_goal,
    "rocm_cuda_score": rocm_cuda_score,
    "gfxarch": gfxarch,
    "rocm_version": rocm_version,
    "rocm_actual_testcount": rocm_actual_testcount,
    "rocm_score": rocm_score,
    "nvarch": nvarch,
    "cuda_version": cuda_version,
    "cuda_actual_testcount": cuda_actual_testcount,
    "cuda_score": cuda_score,
    "version_details": version_details_dict,
    "rocm_cuda_score_details": rocm_cuda_score_details,
    "rocm_score_details": rocm_score_details,
    "cuda_score_details": cuda_score_details
}

# Write to a JSON file
with open('output.json', 'w') as json_file:
    json.dump(output_json, json_file, indent=0, separators=(',', ': '), cls=CustomJSONEncoder)
    
print("output.json file created successfully.")

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
        new_file = 'sample.json'
    else:
        target_dir = stable_dir
        # Handle version formatting for non-latest versions
        version_safe = version.replace('.', '_')
        new_file = f'pytorch_{version_safe}.json'

    # Define the target file path
    target_file_path = os.path.join(target_dir, new_file)

    # Move the file
    shutil.move(file_path, target_file_path)
    print(f"File moved to: {target_file_path}")

# Read and print the JSON file to logs
with open('output.json', 'r') as json_file:
    json_data = json_file.read()
    print("Contents of output.json:")
    print(json_data)

# Execute the function
move_file_based_on_content(json_file_path)
