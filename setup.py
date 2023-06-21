from setuptools import find_packages, setup

setup(
    name="aura-cli",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click", "requests"],
    entry_points="""
        [console_scripts]
        aura=aura.aura:cli
    """,
)