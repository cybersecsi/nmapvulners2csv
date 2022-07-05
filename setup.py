#!/usr/bin/env python3
"""Setup for nmapvulners2csv."""

from setuptools import find_packages, setup
from pathlib import Path

def read(rel_path):
    init = Path(__file__).resolve().parent / rel_path
    return init.read_text('utf-8', 'ignore')

def get_version():
    ver_path = 'nmapvulners2csv/nmapvulners2csv.py'
    for line in read(ver_path).splitlines():
        if line.startswith('VERSION'):
            return line.split('\'')[1]
    raise RuntimeError('Unable to find version string.')

setup(
    name='nmapvulners2csv',
    version='0.0.1',
    description = "Convert Nmap vulners script output to CSV",
    author='SecSI',
    author_email='gaetano.perrone@secsi.io',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Pentesters - Bug Bounty Hunters',
        'Programming Language :: Python :: 3.8',
        'Topic :: Security'
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'nmapvulners2csv = nmapvulners2csv:main'
        ],
    },
    url='https:/github.com/cybersecsi/nmapvulners2csv',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=Path('requirements.txt').read_text().splitlines(),
)