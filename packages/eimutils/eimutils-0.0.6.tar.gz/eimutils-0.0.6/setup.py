from setuptools import setup, find_packages

# ,  find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='eimutils',
    version='0.0.6',
    author='',
    author_email='',
    description='This project is a wrapper library to call utility functions.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.9",
)
