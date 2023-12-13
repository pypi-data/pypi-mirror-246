# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gspreader']

package_data = \
{'': ['*']}

install_requires = \
['gspread>=5.11.3', 'rich>=12.6.0']

setup_kwargs = {
    'name': 'gspreader',
    'version': '0.1.24',
    'description': 'A few helper functions to make gspread even easer to use.',
    'long_description': 'None',
    'author': 'Rivers Cuomo',
    'author_email': 'riverscuomo@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
