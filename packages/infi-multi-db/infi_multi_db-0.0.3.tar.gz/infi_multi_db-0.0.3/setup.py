from setuptools import find_packages, setup

setup(
    name="infi_multi_db",
    packages=find_packages(),
    version="0.0.3",
    description="Package for using multi DBs for Infinity team",
    author="Infinity Team",
    install_requires=[
        "psycopg2",
        # Add other dependencies as needed in the future
    ],
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
