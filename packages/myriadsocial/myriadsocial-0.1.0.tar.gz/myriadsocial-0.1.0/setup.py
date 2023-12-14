from setuptools import setup, find_packages

setup(
    name='myriadsocial',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'pywhatkit',
        'Pillow',  # Pillow is the PIL fork
        'art',     # for ASCII art
        # Include any other Python dependencies
    ],
    entry_points='''
        [console_scripts]
        myriadsocial=myriadsocial.cli:main
    ''',
)
