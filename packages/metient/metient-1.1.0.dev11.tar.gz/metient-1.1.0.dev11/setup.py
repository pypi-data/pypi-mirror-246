from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    #print(requirements)

setup(name='metient', version='1.1.0.dev11', url="https://github.com/divyakoyy/metient.git", packages=['metient', 'metient.util', 'metient.lib'], install_requires=requirements,)
