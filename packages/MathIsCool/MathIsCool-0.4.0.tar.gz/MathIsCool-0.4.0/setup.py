from setuptools import setup, find_packages


with open('README.md') as f:
    desc = f.read()


setup(
    name='MathIsCool',
    version='0.4.0',
    long_description=desc,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'bestErrors>=0.1',
    ]
)