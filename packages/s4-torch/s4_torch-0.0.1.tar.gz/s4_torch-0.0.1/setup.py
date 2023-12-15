# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s4_torch']

package_data = \
{'': ['*']}

install_requires = \
['flax', 'jax', 'swarms', 'torch', 'zetascale']

setup_kwargs = {
    'name': 's4-torch',
    'version': '0.0.1',
    'description': 'S4 - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# s4\n\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/s4',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
