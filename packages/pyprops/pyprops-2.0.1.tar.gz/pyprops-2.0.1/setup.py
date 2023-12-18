from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pyprops',
    version='2.0.1',
    packages=find_packages(),
    py_modules=['pyprops'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)