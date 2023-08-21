from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("test-requirements.txt") as f:
    test_requirements = f.read().splitlines()

# Load the version
version = {}
with open("path/to/version.py") as f:
    exec(f.read(), version)

setup(
    name="aura-cli",
    version=version['__version__'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    tests_require=test_requirements,
    entry_points="""
        [console_scripts]
        aura=aura.aura:cli
    """,
)