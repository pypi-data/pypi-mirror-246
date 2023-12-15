from setuptools import setup, find_packages


with open('README.md') as f:
    desc = f.read()


setup(
    name='MathIsCool',
    version='0.1.0',
    packages=find_packages(),
    long_description=desc,
    long_description_content_type='text/markdown',
)