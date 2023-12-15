# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cm3', 'cm3.utils']

package_data = \
{'': ['*']}

install_requires = \
['SentencePiece',
 'accelerate',
 'bitsandbytes',
 'classifier-free-guidance-pytorch',
 'datasets',
 'deepspeed',
 'einops',
 'lion-pytorch',
 'memory-profiler',
 'numpy',
 'torch',
 'transformers',
 'triton',
 'zetascale']

setup_kwargs = {
    'name': 'cm3',
    'version': '0.2.6',
    'description': 'Description of the cm3 package',
    'long_description': 'None',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
