import setuptools

setuptools.setup(
    name="geonlplify",
    version="0.3.14",
    url="https://github.com/remydecoupes/GeoNLPlify",
    author="Rémy Decoupes",
    author_email="remy.decoupes@inrae.fr",
    description="GeoNLPlify aims to make variations of an input sentence working on spatial information contained in words",
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "spacy>=2.3.0,<=2.3.999",
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