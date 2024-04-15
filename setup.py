from setuptools import setup, find_packages

NAME = "Wrapydb"
VERSION = "0.1.0"
PYTHON_REQUIRES = ">=3.7"
INSTALL_REQUIRES = ["pymysql>=1.0.2", "sqlalchemy>=1.4.22", "sshtunnel>=0.4.0", "pandas>=1.3.0"]

AUTHOR = "tbshiki"
AUTHOR_EMAIL = "info@tbshiki.com"
URL = "https://github.com/tbshiki/" + NAME

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description="A utility for simplified, secure database connections through SSH tunnels using pymysql, sshtunnel, and SQLAlchemy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="Wrapydb, sql, db, ssh",
)
