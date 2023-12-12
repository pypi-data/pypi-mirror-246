import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="harpiamm",
    version="0.0.4",
    author="Lukas Kontenis",
    author_email="lukas.kontenis@lightcon.com",
    description="A Python library for the HARPIA microscopy module.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/lukaskontenis/harpiamm/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'lightcon',
        'spinnaker-python>=2.0.0.147',
        'lklib>=0.0.16'
    ],
    python_requires='>=3.6',
)