from setuptools import setup, find_packages

setup(
    name='automation-fw-setup',
    version='0.1.0',
    url='https://github.com/cccarv82/autotool',
    author='Carlos Carvalho',
    author_email='cccarv82@gmail.com',
    description='A tool for setting up a test automation project with various frameworks and platforms.',
    packages=find_packages(),    
    install_requires=['gitpython', 'colorama'],
)