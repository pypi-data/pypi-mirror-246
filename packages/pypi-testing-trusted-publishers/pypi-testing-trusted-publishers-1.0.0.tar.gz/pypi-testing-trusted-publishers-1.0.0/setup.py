from setuptools import setup, find_packages

setup(
    name='pypi-testing-trusted-publishers',
    version='1.0.0',
    author='Equinor',
    author_email='sesl@equinor.com',
    description='A short description of your package',
    long_description='A longer description of your package. This is just for testing trusted publishers in pypi',
    long_description_content_type='text/markdown',
    url='https://github.com/equinor/pypi-testing-trusted-publishers',
    license='MIT',
    packages=["simplemodule"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)

