from setuptools import setup, find_packages

setup(
    name="nanoswarm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "litellm>=1.20.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "nanoswarm=nanoswarm.cli:main",
        ],
    },
)
