from setuptools import setup, find_packages
setup(
    name="dapc",
    version="3.5.2",
    description="DAPC is a simple audio process python library. This is the first version of Python extension library for dapc.",
    author="Duyu09",
    author_email='qluduyu09@163.com',
    install_requires=[
        'numpy',
        'scipy',
    ],
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
