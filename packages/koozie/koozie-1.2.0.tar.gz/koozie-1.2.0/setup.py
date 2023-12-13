# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['koozie']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pint>=0.18,<0.19']

entry_points = \
{'console_scripts': ['koozie = koozie.cli:koozie_cli']}

setup_kwargs = {
    'name': 'koozie',
    'version': '1.2.0',
    'description': 'A light-weight wrapper around pint for unit conversions.',
    'long_description': '[![Release](https://img.shields.io/pypi/v/koozie.svg)](https://pypi.python.org/pypi/koozie)\n\n[![Test](https://github.com/bigladder/koozie/actions/workflows/test.yaml/badge.svg)](https://github.com/bigladder/koozie/actions/workflows/test.yaml)\n\nkoozie\n======\n\n*koozie* is a light-weight wrapper around [*pint*](https://pint.readthedocs.io/en/stable/) for unit conversions. The intent is to provide much of the functionality without worrying about the setup. It uses quantities internally, but its functions only return floats. This approach reflects the opinion that all calculations should be performed in Standard base SI units, and any conversions can happen via pre- or post-processing for usability. This minimizes additional operations in performance critical code.\n\n*koozie* also defines a few convenient aliases for different units. See the [source code](https://github.com/bigladder/koozie/blob/master/koozie/koozie.py) for details. A list of other available units is defined in [pint\'s default units definition file](https://github.com/hgrecco/pint/blob/master/pint/default_en.txt).\n\nThere are four public functions in *koozie*:\n\n- `fr_u(value, from_units)`: Convert a value (or an iterable container of values) from given units to base SI units\n- `to_u(value, to_units)`: Convert a value (or an iterable container of values) from base SI units to given units\n- `convert(value, from_units, to_units)`: Convert a value (or an iterable container of values) from any units to another units of the same dimensionality\n- `get_dimensionality(units)`: Get a dictionary-like representation of the dimensionality of units. This is useful for checking if two quantities can be converted to common units.\n\nExample usage can be found in the [test file](https://github.com/bigladder/koozie/blob/master/test/test_koozie.py).\n\n*koozie* also provides a command line utility for unit conversions:\n\n```\nUsage: koozie [OPTIONS] VALUE FROM_UNITS [TO_UNITS]\n\n  koozie: Convert VALUE from FROM_UNITS to TO_UNITS.\n\n  If TO_UNITS is not specified, VALUE will be converted from FROM_UNITS into\n  base SI units.\n\nOptions:\n  -v, --version    Show the version and exit.\n  -l, --list TEXT  Print a list of available units by dimension (e.g.,\n                   "power"). Default: list all units.\n  -h, --help       Show this message and exit.\n```\n\nExample usage:\n\n```\n$ koozie 1 inch meter\n> 0.0254 m\n\n$ koozie 0 degC degF\n> 31.999999999999936 °F\n\n$ koozie 0 degC\n> 273.15 K\n\n$ koozie -l flow\n> [length] ** 3 / [time] ([volumetric_flow_rate])\n  -----------------------------------------------\n    - cubic_feet_per_minute (cfm)\n    - gallons_per_minute (gpm)\n\n```\n',
    'author': 'Big Ladder Software',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bigladder/koozie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
