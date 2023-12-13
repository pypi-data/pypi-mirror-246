# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['audioop']

package_data = \
{'': ['*'], 'audioop': ['clinic/*']}

setup_kwargs = {
    'name': 'audioooooooooooooops',
    'version': '0.1.0',
    'description': '',
    'long_description': 'Ripped out audioop out of python repo',
    'author': 'xssfox',
    'author_email': 'xss@sprocketfox.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
