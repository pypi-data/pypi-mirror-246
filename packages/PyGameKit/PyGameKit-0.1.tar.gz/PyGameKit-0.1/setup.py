from setuptools import setup, find_packages

setup (
    name = "PyGameKit",
    version = '0.1',
    packages = find_packages(),
    install_requires = [
        'pygame-ce'
    ]
)