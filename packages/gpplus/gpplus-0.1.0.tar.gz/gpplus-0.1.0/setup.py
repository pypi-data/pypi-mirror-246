from setuptools import setup, find_packages

setup(
    name='gpplus',
    version='0.1.0',
    author='Ramin Bostanabad, Amin Yousefpour',
    author_email='yousefpo@uci.edu',
    description='Python Library for Generalized Gaussian Process Modeling',
    # long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Bostanabad-Research-Group/GP-Plus',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'torch',
        'gpytorch',
        'matplotlib',  
        'sobol_seq',  
        'tabulate',  
	   'botorch',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

