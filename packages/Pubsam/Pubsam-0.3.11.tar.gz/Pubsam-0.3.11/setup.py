from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Pubsam',
    version='0.3.11',
    description='Streamline interaction with the PubChem database. Retrieve and analyze chemical data effortlessly with Pubsam, exploring compounds, substances, assays, proteins, genes, and more. Designed for researchers, scientists, and developers, Pubsam provides a user-friendly interface to access and leverage PubChem’s wealth of information. Dive into molecular analysis, conduct virtual screenings, and unravel chemical features with ease.',
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
