from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='nlp4beginner',
    version='0.0.2',
    description='PYPI tutorial package creation written by Dale Kwon',
    author='Dale Kwon',
    author_email='lk38ll@gmail.com',
    url='https://github.com/mlKwon/crawling',
    long_description='nlp4beginner https://github.com/mlKwon/crawling',
    install_requires=['numpy', 'pandas'],
    packages=find_packages(where='nlp4beginner',exclude=[]),
    # keywords=['mlkwon', 'python datasets', 'python tutorial', 'pypi'],
    python_requires='>=3.9',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)