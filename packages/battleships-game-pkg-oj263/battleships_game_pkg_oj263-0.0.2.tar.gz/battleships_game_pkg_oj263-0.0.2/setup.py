import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="battleships_game_pkg_oj263",
    version="0.0.2",
    author="OJ",
    author_email="oj263@exeter.ac.uk",
    description="A battleships game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ollyjohnson/battleships",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
