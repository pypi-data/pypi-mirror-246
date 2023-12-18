from setuptools import setup, find_packages

import glob

setup(
        name            ="rx_hqm",
        version         ='0.0.3',
        description     ='Project used to extract fitting model in high-q2 bin',
        packages        = ['hqm_data', 'hqm'],
        package_dir     = {'' : 'src'},
        install_requires= open('requirements.txt').read()
        )

