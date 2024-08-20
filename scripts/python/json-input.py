import json
import os
from urllib.parse import urlparse

# Retrieve input parameters from environment variables
schema_version = os.getenv('schema_version', 'V4')
submit_date = os.getenv('submit_date', '2024-08-16')
component_version = os.getenv('component_version', 'pytorch/12.1')
repo_commithash = os.getenv('repo_commithash', 'https://github.com/repo/pytorch/commit/r497th98r7bf87')
rocm_cuda_details = os.getenv('rocm_cuda_details', '98.44/Additional explanations: string')
gfx_rocm = os.getenv('gfx_rocm', 'MI250/6.1')
nvarch_cuda = os.getenv('nvarch_cuda', 'A10G/12.1')
ttg_rat_rs_details = os.getenv('ttg_rat_rs_details', '359944/358763/99.67/Additional explanations: string')
cat_cs_details = os.getenv('cat_cs_details', '359149/99.77/Additinal explanation: string')
version_details = os.getenv('version_details', 'mkl:2024.1,python:3.8')

# Process `component_version`
component, version = component_version.split('/')

# Process `repo_commithash`
parsed_url = urlparse(repo_commithash)
repo = parsed_url.path.split('/commit/')[0]
commit_hash = parsed_url.path.split('/commit/')[1]

# Process `rocm_cuda_details`
rocm_cuda_score, rocm_cuda_score_details = rocm_cuda_details.split('/', 1)

# Process `gfx_rocm`
gfxarch, rocm_version = gfx_rocm.split('/')

# Process `nvarch_cuda`
nvarch, cuda_version = nvarch_cuda.split('/')

# Process `ttg_rat_rs_details`
aisw_test_target_goal, rocm_actual_testcount, rocm_score, rocm_score_details = ttg_rat_rs_details.split('/', 3)

# Process `cat_cs_details`
cuda_actual_testcount, cuda_score, cuda_score_details = cat_cs_details.split('/', 2)

# Process `version_details`
version_details_dict = dict(pair.split(':') for pair in version_details.split(','))

# Construct JSON object
output_json = {
    "schema_version": schema_version,
    "submit_date": submit_date,
    "component": component,
    "version": version,
    "repo": f"https://github.com{repo}",
    "commitHash": commit_hash,
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
    "rocm_cuda_score_details": {"comment": rocm_cuda_score_details},
    "rocm_score_details": {"comment": rocm_score_details},
    "cuda_score_details": {"comment": cuda_score_details}
}

# Write to a JSON file
with open('output.json', 'w') as json_file:
    json.dump(output_json, json_file, indent=4)

print("JSON file created successfully.")
