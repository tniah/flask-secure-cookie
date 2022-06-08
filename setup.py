# -*- coding: utf-8 -*-
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='flask-secure-cookie',
    version='0.3.0',
    author='HaiNT',
    author_email='tronghaibk2008@gmail.com',
    description='An extension for Flask to encrypt/decrypt cookies',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tniah/flask-secure-cookie',
    packages=setuptools.find_packages(),
    install_requires=[
        'cryptography>=37.0.2',
        'flask>=2.1.2'
    ],
    include_package_data=True,
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.7'
)
