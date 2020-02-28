import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="domeneshop-bots",
    version="0.0.1",
    author="Erik Larsen",
    author_email="eriklarsen.post@gmail.com",
    description="Bot for domeneshop.no to keep your dns records updated with correct ip for your self hosting sites and services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/larsensolutions/domeneshop-bots",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)