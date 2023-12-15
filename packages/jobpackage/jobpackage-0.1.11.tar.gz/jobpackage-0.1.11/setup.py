from setuptools import setup, find_packages

setup(
    name='jobpackage',
    version='0.1.11',
    author='Bryn Lom',
    author_email='bryn.lom@edgeglobalsolutions.com',
    description='Package which allows for connection to jobpac using inputs',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)