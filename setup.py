from setuptools import setup, find_packages

setup(
    name="parallel-sort-benchmark",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'streamlit>=1.30.0',
        'pandas>=2.1.0',
        'numpy>=1.24.0',
        'plotly>=5.18.0',
        'psutil>=5.9.0',
        'pytest>=7.4.0',
    ],
)