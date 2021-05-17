from setuptools import setup, find_packages

setup(
    name='PyMPDATA-examples',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=['PyMPDATA @ git+https://github.com/atmos-cloud-sim-uj/PyMPDATA@e70e077#egg=PyMPDATA',
                      'pystrict',
                      'matplotlib',
                      'ipywidgets',
                      'scipy',
                      'pint',
                      'joblib',
                      'sympy',
                      'ghapi'],
    author='https://github.com/orgs/atmos-cloud-sim-uj/people',
    license="GPL-3.0",
    packages=find_packages(include=['PyMPDATA_examples', 'PyMPDATA_examples.*']),
    package_data={'':['*/*/*.txt']},
    include_package_data=True
)
