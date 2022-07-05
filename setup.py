
#!/usr/bin/env python3
"""Setup for nmapvulners2csv."""

from setuptools import find_packages, setup
from pathlib import Path

def read(rel_path, fix_header=False):
    init = Path(__file__).resolve().parent / rel_path
    initial_content = init.read_text('utf-8', 'ignore')
    if fix_header:
        fixed_header = '<h1 align="center"><img src="https://raw.githubusercontent.com/cybersecsi/nmapvulners2csv/main/assets/logo-light-mode.png" alt= "nmapvulners2csv" width="300px"></h1>'
        content = fixed_header + initial_content.split('</h1>')[1]
        return content
    else:
        return initial_content

def get_version():
    ver_path = 'nmapvulners2csv/nmapvulners2csv.py'
    for line in read(ver_path).splitlines():
        if line.startswith('VERSION'):
            return line.split('\'')[1]
    raise RuntimeError('Unable to find version string.')

setup(
    name='nmapvulners2csv',
    version=get_version(),
    description = "Convert Nmap Vulners script output to CSV",
    author='SecSI',
    author_email='info@secsi.io',
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
    long_description=read('README.md', fix_header=True),
    long_description_content_type='text/markdown',
    install_requires=Path('requirements.txt').read_text().splitlines(),
)