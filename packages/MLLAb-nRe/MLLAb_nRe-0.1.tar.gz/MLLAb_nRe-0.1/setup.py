from setuptools import setup, find_packages

setup(
    name='MLLAb_nRe',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.0.0',
        'pandas>=1.0.0',
        'scikit-learn>=0.0',
        'matplotlib>=3.0.0',
        'seaborn>=0.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
