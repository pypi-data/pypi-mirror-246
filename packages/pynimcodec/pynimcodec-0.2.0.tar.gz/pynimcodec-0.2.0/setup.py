# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynimcodec', 'pynimcodec.nimo', 'pynimcodec.nimo.fields']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pynimcodec',
    'version': '0.2.0',
    'description': 'Codecs for Satellite IoT messaging implemented in Python.',
    'long_description': '# pynimcodec\n\nA set of message codecs for use with satellite IoT products implemented\nin Python.\n\n## nimo\n\nThe NIMO message codec was designed by ORBCOMM and represents an efficient\nbinary data packing for various data types at a bit-level.\n\nThis module also provides facilities to build a XML file compliant with the\nORBCOMM and/or Viasat *Message Definition File* concept to apply to messages\nsent over the IsatData Pro service.\n\nThe principles of the NIMO *Common Message Format* are:\n\n* First byte of payload is *Service Identification Number* (**SIN**)\nrepresenting a microservice running on an IoT device.\nEach `<Service>` consists of `<ForwardMessages>` (e.g. commands) and/or\n`<ReturnMessages>` (e.g. reports or responses from the IoT device).\nSIN must be in a range 16..255.\n    \n> [!WARNING]\n> SIN range 16..127 may *conflict* with certain ORBCOMM-reserved messages\n> when using the ORBCOMM IDP service.\n\n* Second byte of payload is *Message Identification Number* (**MIN**)\nrepresenting a remote operation such as a data report or a command.\nThe combination of **SIN** and **MIN** and direction (Forward/Return) enables\ndecoding of subsequent `<Fields>` containing data.\n\n* Subsequent bytes of data are defined by `<Fields>` where each `<Field>` has\na data type such as `<SignedIntField>`, `<EnumField>`, etc.\nThese fields can be defined on individual bitwise boundaries, for example a\n5-bit unsigned integer with maximum value 31, or a boolean single bit.',
    'author': 'geoffbrucepayne',
    'author_email': 'geoff.bruce-payne@inmarsat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inmarsat-enterprise/pynimomodem',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
