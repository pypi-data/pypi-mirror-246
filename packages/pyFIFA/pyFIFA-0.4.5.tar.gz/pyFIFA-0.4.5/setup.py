from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='pyFIFA',
    version='0.4.5',
    py_modules=['main','world_cup','helper_functions','trivia'],
    packages=find_packages(),
    install_requires=[
        'pyfiglet>=0.8.post1',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'pyFIFA-play = main:main',
        ],
    },
    # Other setup parameters...
)
