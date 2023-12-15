from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='puZC',
    version='0.0.111111',
    description='This Python package, PubChemAPI, simplifies the interaction with the PubChem database, allowing users to seamlessly retrieve information related to compounds, substances, assays, proteins, genes, and more. Whether you\'re a researcher, scientist, or developer, this package provides an easy-to-use interface to access a wealth of information stored in PubChem.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Ahmed Alhilal',
    author_email='aalhilal@udel.edu',
    license='MIT',
    classifiers=classifiers,
    keywords='cheminformatics',
    packages=find_packages(),
    install_requires=[
        'lazypredict',
        'rdkit',
        'mordred',
        'ipyplot',
        'ipython',
        'pandas',
        'Pillow',
        'pybase64',
        'requests',
        'statsmodels',
        'fastapi',
        'kaleido',
        'python-multipart',
        'uvicorn',
        'numpy',
        'typing-extensions<4.6.0,>=4.0.0',  # Add or modify this line
        'tensorflow-probability==0.22.0'  # Add or modify this line based on your requirements

    ]
)

