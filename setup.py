from re import search
from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('starkinfra/__init__.py') as f:
    version = search(r'version = \"(.*)\"', f.read()).group(1)

setup(
    name="starkinfra",
    packages=find_packages(),
    include_package_data=True,
    description="SDK to facilitate Python integrations with Stark Infra",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/starkinfra/sdk-python",
    author="Stark Bank",
    author_email="developers@starkinfra.com",
    keywords=["stark infra", "starkinfra", "sdk", "open banking", "openbanking", "banking", "open", "stark"],
    version=version,
    install_requires=[
        "starkbank>=2.14.1",
    ],
)
