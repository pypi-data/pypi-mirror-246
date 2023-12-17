from distutils.core import setup

setup(
    name='cloud_import',
    packages=['cloud_import'],
    version='0.3',
    license='MIT',
    description='Import Python modules straight from the cloud (e.g. GitHub) at runtime!',
    author='Henri J. Norden (originally by James Murphy)',
    #author_email='your.email@domain.com',
    url='https://github.com/Henri-J-Norden/py-cloud-import',
    download_url='https://github.com/Henri-J-Norden/py-cloud-import.git',
    keywords=['CLOUD', 'IMPORT', 'ARBITRARY CODE EXECUTION'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.4',
        #'Programming Language :: Python :: 3.5',
        #'Programming Language :: Python :: 3.6',
    ],
    long_description_content_type='text/markdown',
    long_description="""
Import Python modules straight from the cloud (e.g. GitHub) at runtime!

## Installation
* pip: `pip install cloud_import`
* no pip: copy [cloud_import.py](https://github.com/Henri-J-Norden/py-cloud-import/blob/master/cloud_import/cloud_import.py) into your project

## Usage
See [examples/example1.py](https://github.com/Henri-J-Norden/py-cloud-import/blob/master/examples/example1.py)

## Why?
This can be used to entirely skip the 'deployment' step for internal tooling, not meant for distribution or public usage. 

## Limitations
* No dependency handling
* Fixed URL structure: the source code for module `foo.bar` must be accessible at `<url>/foo/bar/*.py`
* Bad things will happen if the cloud source code changes while a package (with multiple modules) is being imported
 
    """,
)
