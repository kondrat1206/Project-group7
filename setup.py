from setuptools import setup, find_namespace_packages

setup(
    name='assistant',
    version='0.1.0',
    description='Very useful code',
    author='7Team',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['assistant = assistant.main:main']}
)