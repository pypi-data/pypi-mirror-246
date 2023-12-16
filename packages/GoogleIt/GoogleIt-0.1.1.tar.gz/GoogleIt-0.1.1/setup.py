from setuptools import setup, find_packages

setup(
    name='GoogleIt',
    version='0.1.1',
    author='William Renaldy A',
    author_email='williamrenaldy.a@gmail.com',
    description='Python package to search Google powered by PALM 2',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)