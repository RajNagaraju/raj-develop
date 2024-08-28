import json
import os
import shutil

# Retrieve input parameters from environment variables
schema_version = os.getenv('schema_version', 'V4')
submit_date_system_spec = os.getenv('submit_date_system_spec', '2024-08-16/SMC4124')
component_version = os.getenv('component_version', 'pytorch/12.1')
repo_commithash = os.getenv('repo_commithash', 'https://github.com/repo/pytorch/commit/r497th98r7bf87')
gfx_rocm = os.getenv('gfx_rocm', 'MI250/6.1')
nvarch_cuda = os.getenv('nvarch_cuda', 'A10G/12.1')
rocm_ut_fail_pass_skip_deselect_warn_err = os.getenv('rocm_ut_fail_pass_skip_deselect_warn_err', '100/358763/358763/358763/358763/358763')
cuda_ut_fail_pass_skip_deselect_warn_err = os.getenv('cuda_ut_fail_pass_skip_deselect_warn_err', '358763/358763/358763/358763/358763/358763')
version_details = os.getenv('version_details', {"mkl" : "2024.1", "python" : "3.8"})
rocm_score_details = os.getenv('rocm_score_details', {"logurl" : "URL to test log", "artifacturl" : "Link to test artifactory", "comment" : "Additional details about ROCm score"})
cuda_score_details = os.getenv('cuda_score_details', {"logurl" : "URL to test log", "artifacturl" : "Link to test artifactory", "comment" : "Additional details about ROCm score"})

# process `submitdate_systemspect`
submit_date, systemspec = submit_date_system_spec.split('/')

# Process `component_version`
component, version = component_version.split('/')

# Process `repo_commithash`
repo, commithash = repo_commithash.split('/commit/')

# Process `rocm_ut_fail_pass_skip_deselect_warn_err`
rocm_ut_failed, rocm_ut_passed, rocm_ut_skipped, rocm_ut_deselected, rocm_ut_warnings, rocm_ut_errors = rocm_ut_fail_pass_skip_deselect_warn_err.split('/')

# Process `cuda_ut_fail_pass_skip_deselect_warn_err`
cuda_ut_failed, cuda_ut_passed, cuda_ut_skipped, cuda_ut_deselected, cuda_ut_warnings, cuda_ut_errors = cuda_ut_fail_pass_skip_deselect_warn_err.split('/')

# Process `gfx_rocm`
gfxarch, rocm_version = gfx_rocm.split('/')

# Process `nvarch_cuda`
nvarch, cuda_version = nvarch_cuda.split('/')

# Process `version_details`
version_details_dict = json.loads(version_details)

# Process `rocm_score_details`
rocm_score_details_dict = json.loads(rocm_score_details)

# Process `cuda_score_details`
cuda_score_details_dict = json.loads(cuda_score_details)

# Construct JSON object
output_json = {
    "schema_version": schema_version,
    "submit_date": submit_date,
    "component": component,
    "version": version,
    "repo": repo,
    "commitHash": commithash,
    "systemspec" : systemspec,
    "gfxarch": gfxarch,
    "rocm_version": rocm_version,
    "rocm_ut_failed" : rocm_ut_failed,
    "rocm_ut_passed" : rocm_ut_passed,
    "rocm_ut_skipped" : rocm_ut_skipped,
    "rocm_ut_deselected" : rocm_ut_deselected,
    "rocm_ut_warnings" : rocm_ut_warnings,
    "rocm_ut_errors" : rocm_ut_errors,
    "nvarch": nvarch,
    "cuda_version": cuda_version,
    "cuda_ut_failed" : cuda_ut_failed,
    "cuda_ut_passed" : cuda_ut_passed,
    "cuda_ut_skipped" : cuda_ut_skipped,
    "cuda_ut_deselected" : cuda_ut_deselected,
    "cuda_ut_warnings" : cuda_ut_warnings,
    "cuda_ut_errors" : cuda_ut_errors,
    "version_details": version_details_dict,
    "rocm_score_details": rocm_score_details_dict,
    "cuda_score_details": cuda_score_details_dict
}

# Write to a JSON file
with open('output.json', 'w') as json_file:
    json.dump(output_json, json_file, indent=4)
    
print("output.json file created successfully.")

# File paths
json_file_path = 'output.json'
latest_dir = 'docker/ubuntu22/rocm-6.2/'
stable_dir = 'docker/rocm/ubuntu22/6.0/'

# Ensure the directories exist
os.makedirs(latest_dir, exist_ok=True)
os.makedirs(stable_dir, exist_ok=True)

# Function to move the file based on conditions
def move_file_based_on_content(file_path, user_component):
    """
    Move the file based on the content of the JSON file and the user-provided component.

    Args:
        file_path (str): Path to the JSON file.
        user_component (str): Component value provided by the user to match against.
    """
    # Read and parse the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract the relevant values
    component = data.get('component')
    version = data.get('version')

    if component is None or version is None:
        raise ValueError("The JSON file must contain 'component' and 'version' fields.")

    # Check if the component and version meet the condition based on user input
    if component == user_component and version == 'latest':
        target_dir = latest_dir
        new_file = f'{component}.json'  # Use component value to name the file for the latest directory
        print(new_file)
    else:
        target_dir = stable_dir
        # Handle version formatting for non-latest versions
        version_safe = version.replace('.', '_')
        new_file = f'{component}_{version_safe}.json'  # Use component value and formatted version for the stable directory
        print(new_file)

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
move_file_based_on_content(json_file_path, user_component)
