from setuptools import find_packages, setup

with open("BashaFusion/README.md", "r") as f:
    long_description = f.read()

setup(
    name="BashaFusion",
    version="0.0.2",
    description="A package used to convert indic language to iast & iast to inidc langauge viceversa",
    packages=['BashaFusion'],
    package_data={'BashaFusion': ["iast-token.db"]},

#    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
#    keyword='iast'
    url="https://github.com/dankarthik25/BashaFusion",
    author="Dan Karthik",
    author_email="dankarthik25@gmail.com",
    project_urls= {
        "Documentation": "https://dankarthik25.github.io/BashaFusion",
        "Source" : "https://github.com/dankarthik25/BashaFusion",
},
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
#    install_requires=['pysqlite3'],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.9",
)

