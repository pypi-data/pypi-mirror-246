import os
from setuptools import setup, find_packages

base = os.path.dirname(__file__)

long_description = ''
path = os.path.join(base, 'readme.md')
if os.path.exists(path):
    with open(path, encoding='utf-8') as f:
        long_description = f.read()

setup(
    packages=find_packages(),
    name = 'seapeapea',
    version = '0.0.1',
    author = "Stanislav Doronin",
    author_email = "mugisbrows@gmail.com",
    url = 'https://github.com/mugiseyebrows/seapeapea',
    description = 'с++ to python transpiler',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    install_requires = ['lark'],
    include_package_data = True,
    package_data = {
        'seapeapea': ['*.lark'],
    },
    entry_points = {
        'console_scripts': [
            'seapeapea = seapeapea:main'
        ]
    }
)