from setuptools import find_packages, setup

VERSION = "0.1.00"
DESCRIPTION = ""
LONG_DESCRIPTION = ""

setup(
    name="parse-le-beacon",
    version=VERSION,
    author="Thyrasec",
    url="https://github.com/thyrasec/parse-le-beacon",
    author_email="",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'requests',
    ],  # add any additional packages that
    # needs to be installed along with your package
    keywords=["python"],
    classifiers=[],
)