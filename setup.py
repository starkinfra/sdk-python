from re import search
from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('starkinfra/__init__.py') as f:
    version = search(r'version = \"(.*)\"', f.read()).group(1)

setup(
    name="starkinfra",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    description="SDK to facilitate Python integrations with Stark Infra",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/starkinfra/sdk-python",
    author="Stark Infra",
    author_email="developers@starkbank.com",
    keywords=["stark infra", "starkinfra", "sdk", "open banking", "openbanking", "banking", "open", "stark"],
    version=version,
    install_requires=[
        "starkcore>=0.1.0",
    ],
)
