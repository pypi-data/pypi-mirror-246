import setuptools
from ML_medic_kit import __version__

# Read in the requirements.txt file
with open("requirements.txt") as f:
    requirements = []
    for library in f.read().splitlines():
        requirements.append(library)

# this is documentation...
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(

    name="ML_medic_kit",
    # set version number using value read in from __init__()
    version=__version__,
    author="Martha Dinsdale, Holly Manning",
    author_email="md661@exeter.ac.uk",
    license="The MIT License (MIT)",
    description="The Machine Learning Medic Kit is designed to enhance the capabilities of health data scientists tackling binary classification problems",
    # read in from readme.md and will appear on PyPi
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marthadinsdale/hds_ca2",
    packages=setuptools.find_packages(),
    # if true look in MANIFEST.in for data files to include
    include_package_data=True,
    # these are for PyPi documentation
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.9',
    # pip requirements
    install_requires=requirements,
)
