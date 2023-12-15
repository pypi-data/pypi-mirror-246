from setuptools import setup

with open('README.md', 'r') as arq: 
    readme = arq.read()

setup(
    name='mockTestAPI',
    version='0.0.2',
    license='MIT License',
    author='Victor Augusto do Carmo',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='Victoraugustodocarmo32@gmail.com',
    keywords='Dados mocks',
    description='Geração de dados falsos com Json',
    packages=['mockTest'],  
    install_requires=[
        'pydantic',
        'faker',
    ],
)
