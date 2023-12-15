from setuptools import setup

setup(
    name='forsee',
    version='0.0.3',
    packages=['forsee'],
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'c4=forsee.forsee:main',  
        ],
    },
)