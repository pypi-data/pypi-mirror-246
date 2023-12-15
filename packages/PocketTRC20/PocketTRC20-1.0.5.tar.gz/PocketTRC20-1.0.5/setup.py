import os
from PocketTRC20.config import NAME, VERSION
from setuptools import setup


path = os.path.dirname(__file__)
with open(path + '/README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description='Python TRON Blockchain Explorer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Lao',
    url='https://github.com/codelao/Pocket-TRC20',
    license='MIT',
    install_requires=[
        'requests>=2.28.2', 'colorama>=0.4.6', 'progress>=1.6'
    ],
    packages=[
        'PocketTRC20'
    ],
    entry_points={
        'console_scripts': [
            'ptrc20=PocketTRC20.__main__:entry_point'
        ]
    }
)
