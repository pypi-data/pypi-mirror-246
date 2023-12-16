from setuptools import setup,find_packages

setup(
    name='forsee',
    version='0.0.6',
    author='Nikos Tzekas',
    author_email='nt@itec-audio.com',
    description='Exports a compile_commands.json from a Crosscore Project',
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