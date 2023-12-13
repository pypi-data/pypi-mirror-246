import setuptools
from setuptools import setup

# pylint: disable-next=exec-used,consider-using-with
exec(open('databricks_genai/version.py', 'r', encoding='utf-8').read())

install_requires = [
    'databricks-sdk>=0.14.0',
    'typing_extensions>=4.7.1',
    'mosaicml-cli>=0.5.30',
]

extra_deps = {}

extra_deps['dev'] = [
    'build>=0.10.0',
    'isort>=5.9.3',
    'pre-commit>=2.17.0',
    'pylint>=2.12.2',
    'pyright==1.1.256',
    'pytest-cov>=4.0.0',
    'pytest-mock>=3.7.0',
    'pytest>=6.2.5',
    'radon>=5.1.0',
    'twine>=4.0.2',
    'toml>=0.10.2',
    'yapf>=0.33.0',
]

extra_deps['all'] = set(dep for deps in extra_deps.values() for dep in deps)

setup(
    name='databricks-genai',
    version=__version__,  # type: ignore pylint: disable=undefined-variable
    author='Databricks',
    author_email='genai-eng-team@databricks.com',
    description='Interact with the Databricks API from python',
    url=
    'https://docs.mosaicml.com/projects/mcli/en/latest/finetuning/finetuning.html',  # TODO: update with DBX docs
    include_package_data=True,
    package_data={},
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    install_requires=install_requires,
    extras_require=extra_deps,
    python_requires='>=3.9',
    ext_package='databricks_genai',
)
