from setuptools import find_packages, setup

PACKAGE_NAME = "snake_charmer_pftools"

setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    description="Snake Charmer PFTOOLS",
    packages=find_packages(),
    entry_points={
        "package_tools": ["snake_charmer_docs = snake_charmer.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)