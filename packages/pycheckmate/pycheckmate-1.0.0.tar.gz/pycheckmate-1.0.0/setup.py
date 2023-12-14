import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycheckmate",
    description="src is a library designed to analyze Python code for various properties, focusing primarily on the evaluation of code authored by programming novices",
    version="1.0.0",
    author="Annabell Brocker,"   
           "The Learning Technologies Research Group,"
           "RWTH Aachen University",
    author_email="a.brocker@cs.rwth-aachen.de",
    url="https://git.rwth-aachen.de/learntech-lufgi9/public/pycheckmate",
    license="MIT",
    #packages=setuptools.find_packages(where="src"),    # List of all python modules to be installed
                                        # Information to filter the project on PyPi website

    #package_dir={"": "src"},     # Directory of the source code of the package
    #data_files=[(".", ["LICENSE", "README.md"])],
    install_requires=[],                     # Install other dependencies if any
    platforms="any",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',                # Minimum version requirement of the package
    py_modules = ["pycheckmate"]
)
