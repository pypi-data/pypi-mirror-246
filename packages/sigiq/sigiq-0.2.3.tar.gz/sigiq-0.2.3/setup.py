from setuptools import setup, find_packages

setup(
    name='sigiq',
    version='0.2.3',
    packages=find_packages(),
    install_requires=[
        'requests',
        'openai', # Freeze version
    ],
)
