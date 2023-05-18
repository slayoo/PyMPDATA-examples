""" the magick behind ``pip install ...`` """
import os
from setuptools import setup, find_packages


def get_long_description():
    """ returns contents of README.md file """
    with open("README.md", "r", encoding="utf8") as file:
        long_description = file.read()
    return long_description

CI = "CI" in os.environ

setup(
    name='PyMPDATA-examples',
    description='PyMPDATA usage examples reproducing results from literature'
                ' and depicting how to use PyMPDATA in Python from Jupyter notebooks',
    use_scm_version={"local_scheme": lambda _: "", "version_scheme": "post-release"},
    setup_requires=['setuptools_scm'],
    install_requires=['PyMPDATA',
                      'open-atmos-jupyter-utils',
                      'pystrict',
                      'matplotlib',
                      'ipywidgets',
                      'scipy',
                      'pint',
                      'joblib',
                      'sympy',
                      'ghapi'],
    extras_require={
        "tests": [
            "pytest",
            "nbconvert",
            "jupyter-core" + "<5.0.0" if CI else "",
            "jsonschema" + "==3.2.0" if CI else "",  # https://github.com/jupyter/nbformat/issues/232
            "Jinja2" + "<3.0.0" if CI else "",  # https://github.com/jupyter/nbconvert/issues/1568
            "MarkupSafe" + "<2.1.0" if CI else "",  # https://github.com/aws/aws-sam-cli/issues/3661
            "matplotlib" + "<3.6.0" if CI else "",
            "ipywidgets" + "<8.0.3" if CI else "",
        ]
    },
    author='https://github.com/open-atmos/PyMPDATA/graphs/contributors',
    license="GPL-3.0",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=['PyMPDATA_examples', 'PyMPDATA_examples.*']),
    package_data={'': ['*/*/*.txt']},
    include_package_data=True,
    project_urls={
        "Tracker": "https://github.com/open-atmos/PyMPDATA/issues",
        "Documentation": "https://open-atmos.github.io/PyMPDATA-examples",
        "Source": "https://github.com/open-atmos/PyMPDATA-examples"
    }
)
