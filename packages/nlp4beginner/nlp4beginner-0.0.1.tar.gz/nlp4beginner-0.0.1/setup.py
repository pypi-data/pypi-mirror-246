from setuptools import setup, find_packages

setup(
    name='nlp4beginner',
    version='0.0.1',
    description='PYPI tutorial package creation written by Dale Kwon',
    author='Dale Kwon',
    author_email='lk38ll@gmail.com',
    url='https://github.com/mlKwon/crawling',
    install_requires=['numpy', 'pandas'],
    packages=find_packages(where='src',exclude=[]),
    # keywords=['mlkwon', 'python datasets', 'python tutorial', 'pypi'],
    python_requires='>=3.9',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)