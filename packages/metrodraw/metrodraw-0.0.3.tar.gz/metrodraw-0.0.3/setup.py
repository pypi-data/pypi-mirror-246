import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metrodraw",
    version="0.0.3",
    author="Kavi Gupta",
    author_email="metrodraw@kavigupta.org",
    description="Allows you to create metro maps.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kavigupta/metrodraw",
    packages=setuptools.find_packages(),
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["matplotlib==3.7.4"],
)
