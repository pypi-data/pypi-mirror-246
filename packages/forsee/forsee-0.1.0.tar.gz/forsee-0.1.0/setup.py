from setuptools import setup,find_packages

setup(
    name='forsee',
    version='0.1.0',
    author='Nikos Tzekas',
    author_email='nt@itec-audio.com',
    description='Exports a compile_commands.json from a Crosscore Project',
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