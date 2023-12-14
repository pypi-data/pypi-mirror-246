# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netninja']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'zetascale']

setup_kwargs = {
    'name': 'netninja',
    'version': '0.0.1',
    'description': 'Netrunner - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Niva\nBreaching networks with Niva\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Netrunner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
