from setuptools import setup, find_packages

with open("brute/requirements.txt", "r") as f:
    required = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="brute-force-attacker",
    version="1.0.0",
    author="Praveen",
    author_email="mspraveenkumar77@gmail.com",
    description="A wrapper tool for mediainfo tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=required,
    entry_points={
        "console_scripts": ["brute = brute.brute:main"],
    },
)

