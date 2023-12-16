from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'crypto_trader',
    version = '0.0.2',
    long_description = long_description,
    long_description_content_type ='text/markdown',
    description = 'crypto_trader',
    license = 'MIT',
    # author = 'jeakwon',
    # author_email = 'onlytojay@gmail.com',
    # url = 'https://github.com/jeakwon/ypcc',
    # download_url = 'https://github.com/jeakwon/ypcc/archive/0.0.tar.gz',
    install_requires = [],
    packages = find_packages(exclude = []),
    keywords = ['ypcc'],
    python_requires = '>=3',
    package_data = {},
    zip_safe = False,
    classifiers = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)