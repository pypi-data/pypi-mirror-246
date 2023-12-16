from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education'
]

setup(
    name='akash_basic_calculator',
    version='0.0.1',
    description='A very basic calculator',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Akash Singh',
    author_email='akash.singh@proteustech.in',
    license='MIT',
    classifiers=classifiers,
    keywords="calculator",
    packages=find_packages(),
    install_requires = ['']
)