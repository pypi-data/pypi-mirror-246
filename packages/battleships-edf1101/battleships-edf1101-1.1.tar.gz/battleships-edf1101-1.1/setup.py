import setuptools
import os
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = [] # Here we'll add: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="battleships-edf1101",
    version="1.1",
    author="Ed Fillingham",
    author_email="ef494@exeter.ac.uk",
    description="2023 ECM1400 Coursework - Battleships",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/edf1101/Battleships",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['static/images/*', 'templates/*', '*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.4",
    install_requires=install_requires
)