from setuptools import setup, find_packages

# Add your detailed description here
long_description = """A Python script for FTP bruteforcing with asyncio.

Introduction
------------
This script is designed to perform FTP bruteforcing attacks using asyncio. It concurrently attempts to log in to an FTP server using a provided username and a wordlist of passwords.

Disclaimer
----------
This tool is intended for educational and ethical use only. Unauthorized access to computer systems is illegal and strictly prohibited. Use this script at your own risk, and ensure you have proper authorization before attempting any brute-force attacks.

Features
--------
- Asynchronous FTP bruteforcing for improved performance.
- Adjustable concurrency limit to control the number of simultaneous login attempts.
- Progress display during the brute force process.
- User-friendly command-line interface.
"""

setup(
    name='FtpBrutef0rxr',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'aioftp',
        'termcolor',
        'asyncio',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'FtpBrutef0rxr = FtpBrutef0rxr:FtpBrutef0rxr',
        ],
    },
    author='Manoj Prakash',
    author_email='manojprakash.h1@gmail.com',
    description='A Python script for FTP bruteforcing with asyncio.',
    url='https://github.com/CyberMaxGuardian/FtpBrutef0rxr.git',
    long_description=long_description,
    license='MIT',
    include_package_data=True,
    python_requires='>=3.6',
)
