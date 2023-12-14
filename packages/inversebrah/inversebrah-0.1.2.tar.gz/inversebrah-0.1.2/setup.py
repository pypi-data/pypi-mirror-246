from setuptools import setup, find_packages

setup(
    name='inversebrah',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        
        # Include any other Python dependencies
    ],
    entry_points='''
        [console_scripts]
        inversebrah=inversebrah.cli:main
    ''',
)
