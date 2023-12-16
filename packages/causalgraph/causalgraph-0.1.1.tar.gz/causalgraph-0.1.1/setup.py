from setuptools import setup, find_packages

with open("README_PIP.md", "r", encoding="utf-8") as fh:
    # variable will be filled with the README content and used
    # as the long description of the package
    long_description = fh.read()

setup(
    name="causalgraph",
    version="0.1.1",
    author="Fraunhofer IWU",
    author_email="causalgraph@iwu.fraunhofer.de",
    description="A python package for modeling, persisting and visualizing causal graphs embedded in knowledge graphs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=[
        "*tests*",
        '*pycache*'
    ]),
    package_data={
        #'causalgraph.learn': ['*','*/*','*/*/*'],
        'causalgraph.store': ['*','*/*','*/*/*'],
        'causalgraph.utils': ['*','*/*','*/*/*'],
        'data.logs': ['*','*/*','*/*/*'],
        'data': ['*','*/*','*/*/*'],
        'config': ['*','*/*','*/*/*']
    },
    include_package_data=True,
    exclude_package_data={'': ['*__pycache__*']},
    install_requires=[
        'owlready2==0.43',
        'networkx==2.8.4',
        'matplotlib==3.5.1',
        'ecs_logging==1.1.0',
        'numpy==1.23.5',
        'deprecated==1.2.14'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]
)