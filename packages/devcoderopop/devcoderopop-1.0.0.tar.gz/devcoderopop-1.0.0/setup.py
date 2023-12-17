from setuptools import setup, find_packages 
  
setup( 
    name='devcoderopop', 
    version='1.0.0', 
    description='dcoder is op', 
    author='divyansh', 
    author_email='akashsah2003@gmail.com', 
    packages=['sbomgen', 
            'sbomgen.Parsers', 
            'sbomgen.Utility'
            ], 
    install_requires=[ 
        'datetime',
        'argparse',
        'toml'
    ],
    entry_points= {
        'console_scripts': [
            'sbomgen = sbomgen.main:main',
        ],
    },
) 