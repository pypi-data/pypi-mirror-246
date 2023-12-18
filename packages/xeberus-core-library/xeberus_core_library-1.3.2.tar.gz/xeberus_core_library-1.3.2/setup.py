# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode',
 'majormode.xeberus',
 'majormode.xeberus.constant',
 'majormode.xeberus.model']

package_data = \
{'': ['*']}

install_requires = \
['perseus-core-library>=1.19,<2.0']

setup_kwargs = {
    'name': 'xeberus-core-library',
    'version': '1.3.2',
    'description': 'Xeberus Core Python Library',
    'long_description': '# Xeberus Core Python Library\n\nXeberus Core Python Library is a repository of reusable Python components to be shared by some Python projects using the Xeberus RESTful API.\n\nThese components have minimal dependencies on other libraries, so that they can be deployed easily.  In addition, these components will keep their interfaces as stable as possible, so that other Python projects can integrate these components without having to worry about changes in the future.\n',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/majormode/xeberus-core-python-library',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
