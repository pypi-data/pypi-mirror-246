from setuptools import setup

setup(
    name='bruteforce_script',
    version='1.0',
    packages=[],
    install_requires=[
        'requests',
        'argparse',
        'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'bruteforce_script = bruteforce_script:main',
        ],
    },
)
