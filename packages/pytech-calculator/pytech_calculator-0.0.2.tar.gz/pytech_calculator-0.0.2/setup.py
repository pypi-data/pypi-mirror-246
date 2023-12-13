
from setuptools import setup, find_packages

VERSION = "0.0.2"
DESCRIPTION = "The first package for PyTech"
LONG_DESCRIPTION = "We are embarking on a journey to create our very first simple python package."

setup(
    name="pytech_calculator",
    version=VERSION,
    author="Mario Simunic",
    author_email="marsim@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires= [],  #  any additional packages used in our code, installed alongside our package
    keywords=["python", "calculator", "math"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
