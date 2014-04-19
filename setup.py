from setuptools import setup


def readme():
    """
    Extrats contents from README.md

    """
    with open('README.md') as r:
        return r.read()


def requirements():
    """
    Extracts contents from requirements.txt

    """
    with open('requirements.txt') as r:
        return r.read()


setup(
    name='pepperstack',
    version='0.0.1',
    description='Pepperstack is a host inventory tool',
    long_rescription=readme(),
    author='Matthieu Rosinski',
    classifiers = [
        'Programming Language :: Python :: 2.7',
        ],
    packages = [
        'pepperstack'
        ],
    install_requires=requirements(),
    )
