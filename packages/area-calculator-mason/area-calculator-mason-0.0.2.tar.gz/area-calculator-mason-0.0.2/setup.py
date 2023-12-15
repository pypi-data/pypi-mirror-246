from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="area-calculator-mason",                             # This is the name of the package
    version="0.0.2",                                        # The initial release version
    author="Mason Mapfundematsva",                              # Full name of the author
    author_email="masonmapfunde@gmail.com",
    description="Calculate areas of geometrical figures",
    long_description=long_description,                      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=find_packages(),                    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                                      # Information to filter the project on PyPi website
    # python_requires='>=3.6',                                # Minimum version requirement of the package
    py_modules=["area_calculator_dci"],                     # Name of the python package
    # package_dir={'': 'area-calculator-dci'},             # Directory of the source code of the package
    install_requires=[]                                     # Install other dependencies if any
)
