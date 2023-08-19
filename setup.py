from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


with open("test-requirements.txt") as f:
    test_requirements = f.read().splitlines()

setup(
    name="aura-cli",
    version="0.2.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    tests_require=test_requirements,
    entry_points="""
        [console_scripts]
        aura=aura.aura:cli
    """,
)