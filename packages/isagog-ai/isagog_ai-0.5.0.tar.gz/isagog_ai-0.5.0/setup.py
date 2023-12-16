# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['client', 'isagog', 'isagog.client', 'isagog.model', 'model']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.4.3,<8.0.0',
 'rdflib>=7.0.0,<8.0.0',
 'requests>=2.31.0,<3.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'isagog-ai',
    'version': '0.5.0',
    'description': '',
    'long_description': '# isagog-ai-cli\nClient for isagog ai services\n',
    'author': 'Guido Vetere',
    'author_email': 'g.vetere@isagog.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
