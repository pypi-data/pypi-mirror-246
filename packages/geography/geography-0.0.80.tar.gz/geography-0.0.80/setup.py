from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]

setup(
    name="geography",
    version="0.0.80",
    description="Get info about countries and states",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    author="FrenchFries8854",
    author_email="frenchfries8854@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="geography",
    packages=find_packages(),
    install_requires=[""]
)
