from setuptools import find_packages, setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='layout_cnab_240',
    version='1.0',
    author='AdanEinstein',
    author_email='adaneinstein@gmail.com',
    description = "Utility class to build batch file",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages=find_packages()
)