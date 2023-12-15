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
    version='0.3.1111',
    description='Streamline interaction with the PubChem database. Retrieve and analyze chemical data effortlessly with Pubsam, exploring compounds, substances, assays, proteins, genes, and more. Designed for researchers, scientists, and developers, Pubsam provides a user-friendly interface to access and leverage PubChem’s wealth of information. Dive into molecular analysis, conduct virtual screenings, and unravel chemical features with ease.',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',  # Specify the content type as markdown
    url='https://github.com/yourusername/pubsam',  # Replace with your actual GitHub repository URL
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
        'typing-extensions<4.6.0,>=4.0.0',
        'tensorflow-probability==0.22.0',
    ],
    entry_points={
        'console_scripts': [
            'pubsam-cli=pubsam.cli:main',
        ],
    },
)
