from setuptools import setup, find_packages

setup(
    name='tokybook_audiobook_fetcher',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4 == 4.12.2',
        'requests == 2.31.0',
        'tqdm == 4.66.1',
        'urllib3 == 2.1.0'
    ],
    entry_points={
        'console_scripts': [
            'tokybook-audiobook-fetcher = tokybook_audiobook_fetcher.main:main_function',
        ],
    },
)
