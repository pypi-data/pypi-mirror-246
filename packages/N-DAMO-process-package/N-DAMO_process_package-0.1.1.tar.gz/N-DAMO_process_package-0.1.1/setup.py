from setuptools import setup, find_packages

setup(
    name='N-DAMO_process_package',
    version='0.1.1',
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
           'function=app:main',
        ],
    },
    package_data={
        '': ['function/*.py'],
    },
    license='MIT'
)