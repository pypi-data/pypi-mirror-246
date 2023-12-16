from setuptools import find_packages, setup

with open("IastFramework/README.md", "r") as f:
    long_description = f.read()

setup(
    name="IastFramework",
    version="0.0.6",
    description="A package used to convert indic language to `iast` and `iast` to inidc langauge viceversa",
    packages=['IastFramework'],
    package_data={'IastFramework': ["iast-token.db"]},

#    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
#    keyword='iast'
    url="https://github.com/dankarthik25/IastFramework",
    author="Dan Karthik",
    author_email="dankarthik25@gmail.com",
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

