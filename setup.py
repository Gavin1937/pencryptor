from setuptools import setup, find_packages

# load __version__.py
version = {}
with open('./pencryptor/__version__.py', 'r', encoding='utf-8') as file:
    exec(file.read(), version)

# load README.md
readme = ''
with open('README.md', 'r', encoding='utf-8') as file:
    readme = file.read()

# load requirements.txt
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as file:
    requirements = [i.strip() for i in file.readlines() if i != '\n']

setup(
    name='pencryptor',
    version=version['__version__'],
    author='Gavin1937',
    description='pencryptor: Pack files and encrypt them with 7zip',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=['pencryptor'],
    install_requires=requirements,
)
