import setuptools

setuptools.setup(
    name="geonlplify",
    version="0.3.15",
    url="https://github.com/remydecoupes/GeoNLPlify",
    author="Rémy Decoupes",
    author_email="remy.decoupes@inrae.fr",
    description="GeoNLPlify aims to make variations of an input sentence working on spatial information contained in words",
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "spacy==3.4.2",
        "tokenizers==0.12.1",
        "importlib-metadata>=3.7.0,<=3.999",
        "typing-extensions>=3.7.4,<=3.999",
        "transformers==4.21.3",
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)