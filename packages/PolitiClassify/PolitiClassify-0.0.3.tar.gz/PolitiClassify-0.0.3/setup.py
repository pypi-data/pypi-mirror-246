
from setuptools import find_packages, setup


# Package meta-data.
VERSION = '0.0.3'
NAME = 'PolitiClassify'
DESCRIPTION = "Classify Twitter users' political orientation based on their multiple tweets"
URL = 'https://github.com/LingshuHu/PolitiClassify'
EMAIL = 'lingshu.hu@hotmail.com'
AUTHOR = 'Lingshu Hu'
REQUIRES_PYTHON = '>=3.6.0'

# What packages are required for this module to be executed?
def list_reqs(fname='requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=list_reqs(),
    extras_require={},
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
