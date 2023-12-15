from setuptools import setup, find_packages

setup(
    name="darwin-fiftyone",
    version="1.0.1",
    description="Integration between V7 Darwin and Voxel51",
    author="Simon Edwardsson & Mark Cox-Smith",
    packages=find_packages(),
    url="https://github.com/v7labs/darwin_fiftyone",
    install_requires=[
        "darwin-py",
        "fiftyone"
    ],
)