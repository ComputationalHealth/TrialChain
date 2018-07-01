from setuptools import setup, find_packages

setup(
    name='AssetChecker',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    namespace_packages=['checker'],
    install_requires=[
        'requests',
        'pyfiglet'
    ],
    entry_points={
        'console_scripts': [
            'check-asset = checker.main:check_asset',
        ]
    },
)
