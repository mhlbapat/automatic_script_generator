# flake8: noqa E501

from setuptools import setup

setup(
    name="automatic_script_generator",
    version="0.0.1",
    description="Generate high-throughput scripts automatically",
    maintainer="Mehul Bapat",
    maintainer_email="mbapat@andrew.cmu.edu",
    license="GPL",
    packages=["automatic_script_generator"],
    scripts=["automatic_script_generator/bin/create_files.py"],
    long_description="""
      Generation of high-throughput scripts from excel sheet and base script""",
)
