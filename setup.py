from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='graphite_asap',
    version='0.0.1',
    packages=['graphite_asap'],
    license='Apache 2',
    author='bo',
    author_email='bblanton@underarmour.com',
    description='Graphite API ASAP function hooks',
    long_description=read('README.md'),
    install_requires=['numpy', 'six', 'graphite_api'],
    requires=[],
    test_suite='tests',
    zip_safe=False,
    platforms='any',
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Development Status :: 3 - Alpha",
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: System :: Monitoring',
        "License :: OSI Approved :: Apache Software License",
    )
)
