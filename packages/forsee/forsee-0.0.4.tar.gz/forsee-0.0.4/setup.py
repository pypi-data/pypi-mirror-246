from setuptools import setup,find_packages

setup(
    name='forsee',
    version='0.0.4',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'c4=forsee.forsee:main',  
        ],
    },
)