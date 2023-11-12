from setuptools import setup

setup(
    name='assistant',
    version='0.1.0',
    entry_points={
        'console_scripts': [
            'assistant = assistant.main:main'
        ]
    }
)