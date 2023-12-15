from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Kuantsol Exploratory Data Analysis Package'
LONG_DESCRIPTION = 'Kuantsol Exploratory Data Analysis Package'

# Setting up
setup(
    name="kuantsol-eda",
    version=VERSION,
    author="Barış Coşkun",
    author_email="<baris.coskun@kuantsol.ai>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that

    keywords=['python', 'kuantsol-eda'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)