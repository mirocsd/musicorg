from setuptools import setup, find_packages

setup(
    name="musicorg",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "musicorg = main:main"
        ]
    }
)