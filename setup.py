import sys

from setuptools import setup, find_packages
from setuptools.command.test import test


class PyTest(test):
    user_options = [('args=', 'a', 'arguments for pytest')]
    args = ''

    def initialize_options(self):
        super().initialize_options()

    def run_tests(self):
        import pytest
        import shlex

        error = pytest.main(shlex.split(self.args))
        sys.exit(error)


with open('requirements.txt') as fp:
    install_requires = fp.readlines()


with open('README.md') as fp:
    readme = fp.read()


setup(
    name='lucidtech-las-cli',
    version='0.0.7',
    description='Command Line Interface for Lucidtech AI Services',
    long_description=readme,
    license='Apache 2.0',
    platforms='Posix; MacOS X; Windows',
    author='Lucidtech',
    maintainer='August Kvernmo',
    maintainer_email='august@lucidtech.ai',
    url='https://github.com/LucidtechAI/las-cli',
    packages=find_packages(exclude=['tests']),
    scripts=['bin/las'],
    install_requires=install_requires,
    tests_require=[
        'pytest',
        'requests'
    ],
    cmdclass={'pytest': PyTest},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
    ]
)
