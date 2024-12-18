from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py_resource_manager",
    version="0.1.4",
    author="Dariusz Łabaj",
    author_email="dareklabaj@gmail.com",
    description="Module for handling resources for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,  # Make sure this is set
    package_data={
        # Include stub files
        'py_resource_manager': ['*.pyi'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
    ],
)
