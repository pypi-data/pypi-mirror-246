from setuptools import setup, find_packages

setup (
    name = "pyjeb",
    version = "0.1.3",
    description="A lightweight library to check and variabilize your configuration files",
    long_description="""\
        PyJeb is a lightweight library to check and variabilize your configuration files.

        You can use it for help the parametrization and controle of your configuration file.
        """,
    url="https://github.com/CSharplie/pyjeb/",
    project_urls={
        "Bug Tracker": "https://github.com/CSharplie/pyjeb/issues",
        "CI": "https://github.com/CSharplie/pyjeb/actions",
        "Documentation": "https://github.com/CSharplie/pyjeb",
        "Source Code": "https://github.com/CSharplie/pyjeb",
    },
    download_url="https://pypi.org/project/pyjeb/",
    platforms="Any",
    python_requires=">=3.6",
    license= "Apache License 2.0",
    packages = find_packages(),
)