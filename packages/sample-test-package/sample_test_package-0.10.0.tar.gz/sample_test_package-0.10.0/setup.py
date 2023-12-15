import pathlib
from setuptools import setup, find_packages
here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")
setup(
    name='sample_test_package',
    version='0.10.0',
    author='Suraj Patidar',
    author_email='suraj.pysquad@gmail.com',
    description="Django Waffle Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
