from setuptools import setup, find_packages

setup(
    name='automation-fw-setup',
    version='0.1.1',
    url='https://github.com/cccarv82/autotool',
    author='Carlos Carvalho',
    author_email='cccarv82@gmail.com',
    description='A tool for setting up a test automation project with various frameworks and platforms.',
    packages=find_packages(),    
    install_requires=['gitpython', 'colorama'],
    entry_points={
        'console_scripts': [
            'automation_fw_setup=automation_fw_setup.__main__:main',
        ],
    },
    classifiers=[
        # Classificadores de pacotes ajudam as pessoas a encontrar o seu pacote
        # e podem ser usados por ferramentas automatizadas para fornecer
        # funcionalidades específicas do pacote.
        #
        # Veja: https://pypi.org/classifiers/
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)