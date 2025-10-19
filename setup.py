from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='pygrowup_cdc_calculator',
    version='0.1.0',
    packages=find_packages(),
    package_data={'pygrowup_cdc_calculator': ['cdc_data/*.csv']},
    include_package_data=True,
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'scipy>=1.7.0',
        # Remove pygrowup2 dependency to avoid naming conflict
    ],
    author='Frederick Gyasi',
    author_email='gyasi@musc.edu',
    description='Growth calculator integrating WHO (pygrowup2) and CDC standards for z-scores and percentiles',
    long_description=open('README.md').read() if Path('README.md').exists() else 'Growth calculator for pediatric measurements',
    long_description_content_type='text/markdown',
    url='https://github.com/gyasifred/pygrowup_cdc_calculator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
