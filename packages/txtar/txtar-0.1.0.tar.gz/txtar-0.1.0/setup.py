# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['txtar']

package_data = \
{'': ['*']}

install_requires = \
['pyfakefs>=5.3.2,<6.0.0']

setup_kwargs = {
    'name': 'txtar',
    'version': '0.1.0',
    'description': "Port of golang's [txtar](https://pkg.go.dev/golang.org/x/tools/txtar)",
    'long_description': None,
    'author': 'david',
    'author_email': 'davidventura27@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidventura/txtar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
