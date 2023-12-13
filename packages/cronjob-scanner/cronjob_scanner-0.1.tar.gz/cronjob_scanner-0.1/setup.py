from setuptools import setup, find_packages

setup(
    name='cronjob_scanner',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'cronjob_scanner=cronjob_scanner.cron_collector:main'
        ]
    }
)