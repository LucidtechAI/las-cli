from setuptools import setup


with open('requirements.txt') as fp:
    install_requires = fp.readlines()


with open('README.md') as fp:
    readme = fp.read()


setup(
    name='lucidtech-las-cli',
    version='1.0.0',
    description='CLI for Lucidtech AI Services',
    long_description=readme,
    license='Apache 2.0',
    platforms='Posix; MacOS X; Windows',
    author='Lucidtech',
    maintainer='August Kvernmo',
    maintainer_email='august@lucidtech.ai',
    url='https://github.com/LucidtechAI/las-cli',
    packages=['lascli'],
    entry_points={
        'console_scripts': [
            'las = lascli.__main__:main'
        ]
    },
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet'
    ]
)
