from setuptools import setup, find_packages
from src.kel_package import __version__ as kel_version

with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="kel_package",
    version=kel_version.__version__,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    url="https://kel.qainsights.com",
    license="MIT",
    author="NaveenKumar Namachivayam",
    data_files=[("", ["requirements.txt", "config.toml"])],
    author_email="",
    description="AI assistant in your CLI.",
    install_requires=required,
    entry_points={
        "console_scripts": [
            "kel_package = kel_package.__main__:main",
        ],
    },
)
