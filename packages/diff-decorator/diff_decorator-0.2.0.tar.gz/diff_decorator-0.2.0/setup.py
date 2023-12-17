from setuptools import setup, find_packages

setup(
    name="diff_decorator",
    version="0.2.0",
    packages=find_packages(),
    description="A decorator for diffing outputs in Python tests",
    author="Walid Shouman",
    author_email="eng.walidshouman@gmail.com",
    url="https://github.com/weshouman/py-diff-decorator",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

