import os
import setuptools

with open('README.md', 'r') as f:
    readme_file = f.read()

REPO_NAME = "End_To_End_MLops"
AUTHOR_USERNAME = "kuralamuthan300"

setuptools.setup(
    name = "software_defect_prediction",
    version = "0.0.0",
    author = AUTHOR_USERNAME,
    author_email = "kuralamuthan300@gmail.com",
    description = ("Machine learning application to predict software defects"),
    license = "BSD",
    keywords = "Machine Learning",
    url = "https://github.com/"+AUTHOR_USERNAME+"/"+REPO_NAME,
    long_description=readme_file,
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"}
)