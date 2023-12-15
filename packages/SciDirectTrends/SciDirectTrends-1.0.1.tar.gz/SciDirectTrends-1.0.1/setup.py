import setuptools
from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SciDirectTrends",
    version="1.0.1",
    license="MIT",
    author="AliReza Beigy",
    author_email="alireza.beigy.rb@gmail.com",
    description="A tool for fetching and visualizing publication trends from ScienceDirect",
    entry_points={
        "console_scripts": [
            "scidirecttrends=scidirecttrends.main:main",
        ]
    },
    python_requires=">=3.6",
    platforms=["nt", "posix"],
    long_description=long_description,
    packages=setuptools.find_packages(),
    url="https://github.com/AliRezaBeigy/SciDirectTrends",
    long_description_content_type="text/markdown",
    install_requires=[
        "requests",
        "matplotlib",
        "seaborn",
        "numpy"
    ],
    keywords="ScienceDirect, data visualization, publication trends",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)