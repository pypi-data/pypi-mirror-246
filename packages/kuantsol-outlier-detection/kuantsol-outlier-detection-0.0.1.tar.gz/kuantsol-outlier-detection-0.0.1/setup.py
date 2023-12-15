from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Kuantsol Outlier Detection Package'
LONG_DESCRIPTION = 'Kuantsol Outlier Detection Package'

# Setting up
setup(
    name="kuantsol-outlier-detection",
    version=VERSION,
    author="Barış Coşkun",
    author_email="<baris.coskun@kuantsol.ai>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that

    keywords=['python', 'kuantsol-outlier-detection'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)