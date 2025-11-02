from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''

setup(
    name='pygrowup-cdc-calculator',
    version='0.1.0',
    packages=find_packages(),
    package_data={'pygrowup_cdc_calculator': ['cdc_data/*.csv']},
    include_package_data=True,
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'scipy>=1.7.0',
    ],
    extras_require={
        'who': ['pygrowup2'],
        'dev': [
            'pytest>=6.0',
            'pytest-cov',
            'black',
            'flake8',
            'mypy',
            'isort',
        ],
    },
    author='Frederick Gyasi',
    author_email='gyasi@musc.edu',
    description='Growth calculator integrating WHO (pygrowup2) and CDC standards for z-scores and percentiles',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gyasifred/pygrowup_cdc_calculator',
    project_urls={
        'Bug Reports': 'https://github.com/gyasifred/pygrowup_cdc_calculator/issues',
        'Source': 'https://github.com/gyasifred/pygrowup_cdc_calculator',
        'Documentation': 'https://github.com/gyasifred/pygrowup_cdc_calculator#readme',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='pediatrics growth cdc who z-score percentile anthropometry medical health',
    python_requires='>=3.6',
    zip_safe=False,
)
