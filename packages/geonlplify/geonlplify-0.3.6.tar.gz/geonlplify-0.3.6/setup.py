import setuptools

setuptools.setup(
    name="geonlplify",
    version="0.3.6",
    url="https://github.com/remydecoupes/GeoNLPlify",
    author="Rémy Decoupes",
    author_email="",
    description="GeoNLPlify aims to make variations of an input sentence working on spatial information contained in words",
    # long_description=open('pypi.md').read(),
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas",
        "requests",
        'spacy>=2.3.0,<=2.3.999',
        'importlib-metadata>=3.7.0,<=3.999',
        'typing-extensions>=3.7.4,<=3.999',
        'transformers>=3.4.0,<=4.15.999',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    # package_data={'': ['pypi.md']},
)