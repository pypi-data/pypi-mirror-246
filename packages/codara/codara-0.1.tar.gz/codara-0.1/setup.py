from setuptools import setup, find_packages


# Function to read the list of dependencies from requirements.txt
def read_requirements():
    with open('./requirements.txt') as req:
        return req.read().splitlines()


setup(
    name="codara",
    version="0.1",
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "codara=package.app:main"
        ]
    }
)
