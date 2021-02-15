from setuptools import setup, find_packages


setup(
    name='spotifyapp',
    version='1.0.0',
    install_requires=[
        'requests',
        'flask'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
        ]
    }
)
