from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='nuttypy',
    version='0.0.1',
    install_requires=['boto3', 'psycopg2-binary'], # TODO
    description='Simple functions for accessing AWS Redshift and S3',
    py_modules=['nuttypy'],
    package_dir={'': 'NuttyPy'},
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: MIT',
        'Operating System :: OS Independent',
    ],
    url='https://github.com/nickbuker/nuttypy',
    author='Nick Buker',
    author_email='nickbuker@gmail.com',
)
