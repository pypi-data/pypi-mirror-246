from setuptools import setup, find_packages
from main import main


with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='pyFIFA',
    version='0.4.2',
    packages=find_packages(),
    install_requires=[
        'pyfiglet>=0.8.post1',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'pyFIFA_play = main:main',
        ],
    },

    # Other setup parameters...
)
