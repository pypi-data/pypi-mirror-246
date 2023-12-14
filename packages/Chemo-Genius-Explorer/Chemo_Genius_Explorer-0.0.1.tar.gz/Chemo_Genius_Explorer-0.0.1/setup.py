from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Chemo_Genius_Explorer',
    version='0.0.1',
    description='This Python package, Chemo_Genius_Explorer',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/ahmed1212212/PubChemPyTools.git',  # Replace with your actual repository URL
    author='Ahmed Alhilal',
    author_email='aalhilal@udel.edu',
    license='MIT',
    classifiers=classifiers,
    keywords='Cheminformatics',
    packages=find_packages(),
    install_requires=[
        'rdkit',
        'Pillow',
        'ipython',
        'mordred',
        'pandas',
        'statsmodels',
        'matplotlib'
        'lazypredict', 'rdkit', 'mordred', 'pubsams']
)
