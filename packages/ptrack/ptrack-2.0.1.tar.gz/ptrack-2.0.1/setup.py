from setuptools import setup, find_packages

setup(
    name='ptrack',
    version="2.0.1",
    description='A simple CLI utility for asthetically tracking progress when copying, moving or downloading files.',
    author='Connor Etherington',
    author_email='connor@concise.cc',
    packages=find_packages(),
    install_requires=[
        'rich',
        'argparse',
        'requests',
        'validators',
        'setuptools',
        'humanize',
    ],
    entry_points={
        'console_scripts': [
            'ptc=ptrack.main:copy',
            'ptm=ptrack.main:move',
            'ptd=ptrack.main:download',
            'ptrack=ptrack.main:main',
        ]
    }
)
