import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wordle_saperoi",
    version="0.2.1.1",
    author="Saperoi",
    author_email="uesugi.sapero@gmail.com",
    description="A python-based customizable Wordle engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saperoi/wordle-py",
    project_urls={
        "Bug Tracker": "https://github.com/saperoi/wordle-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    packages=['wordle_engine'],
    python_requires=">=3.6",
)
