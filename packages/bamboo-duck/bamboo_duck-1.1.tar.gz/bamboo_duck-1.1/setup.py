from setuptools import setup, find_packages

setup(
    name='bamboo_duck',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'duckdb',
        'PyYAML',
        'networkx',
        'matplotlib',
        'parsimonious',
        'dataclasses; python_version<"3.7"'
    ],
    entry_points={
        'console_scripts': [
            'bamboo_duck=bamboo_duck.main:cli',   # "mycli" will be the command users type in their terminal.
        ],
    }
)
