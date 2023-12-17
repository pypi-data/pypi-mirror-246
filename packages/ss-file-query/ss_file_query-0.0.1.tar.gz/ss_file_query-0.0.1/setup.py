from setuptools import find_packages, setup

PACKAGE_NAME = "ss_file_query"

setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    description="Semi-structured file query tool",
    packages=find_packages(),
    entry_points={
        "package_tools": ["query_tool = ss_file_query.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)