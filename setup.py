#!/usr/bin/env python3
# vim: fileencoding=utf-8 expandtab shiftwidth=4
'''
r_u_done_yet_syncthing: Are you done yet Syncthing?

Copyright 2018-, Simon Lundström <simmel@soy.se>.
Licensed under the ISC license.
'''

import sys
from setuptools import setup, find_packages
import json

version = "1.0.0"

require_envs = ['default', 'develop']
requires = { env: [] for env in require_envs }
try:
    pipfile = json.load(open('Pipfile.lock'))

    for env in require_envs:
        for package, metadata in pipfile[env].items():
            if 'version' in metadata:
                requires[env].append(package+metadata['version'])
except FileNotFoundError:
    pass

setup(
    name="r_u_done_yet_syncthing",
    version=version,
    description="Check if Syncthing has synced a device recently",
    long_description=open("README.md").read(),
    author="Simon Lundström",
    author_email="simmel@soy.se",
    url="https://github.com/simmel/r_u_done_yet_syncthing",
    license="ISC license",
    entry_points={
        'console_scripts': [
	    'r_u_done_yet_syncthing=r_u_done_yet_syncthing:main',
        ],
    },
    install_requires=requires['default'],
    extras_require={
        'develop': requires['develop'],
    },
    py_modules=['r_u_done_yet_syncthing'],
)
