from setuptools import setup, find_packages

import glob

setup(
        name            ='rx_monitor',
        version         ='0.0.1',
        description     ='Project used to carry out several checks',
        scripts         = glob.glob('scripts/*'),
        packages        = ['monitor', 'monitor_data'],
        package_dir     = {'' : 'src'},
        install_requires= open('requirements.txt').read()
        )


