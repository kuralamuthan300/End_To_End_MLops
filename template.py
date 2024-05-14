import os
from pathlib import Path

project_name = "software_defect_prediction"
project_path = 'C:/Users/kural/Desktop/Projects/End_To_End_MLops/'

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "app.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "templates/index.html",
    "test.py"
]

for single_file in list_of_files:
    single_file = project_path + single_file
    file_directory, file_name = os.path.split(single_file)
    
    if( file_directory !="" or not os.path.exists(file_directory)):
        os.makedirs(file_directory, exist_ok=True)    
    
    if(os.path.exists(single_file)):
        print(f"File : {single_file} exists")
    else:
        open(single_file, "x")
        print(f"File : {single_file} created successfully")
        