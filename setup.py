from setuptools import setup, find_packages

setup(
    name='PyMPDATA-examples',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=['PyMPDATA @ git+https://github.com/atmos-cloud-sim-uj/PyMPDATA@0ea4af5#egg=PyMPDATA',
                      'pystrict>=1.1',
                      'matplotlib>=3.2.1',
                      'ipywidgets>=7.5.1',
                      'scipy>=1.4.1',
                      'pint>=0.16.1',
                      'joblib>=0.14.1',
                      'sympy>=1.6.1',
                      'ghapi'],
    author='https://github.com/orgs/atmos-cloud-sim-uj/people',
    license="GPL-3.0",
    packages=find_packages(include=['PyMPDATA_examples', 'PyMPDATA_examples.*']),
    package_data={'':['*/*/*.txt']},
    include_package_data=True
)
