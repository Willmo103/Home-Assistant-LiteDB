from setuptools import setup, find_packages

setup(
    name='home_assistant_litedb',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'home_assistant_litedb=home_assistant_litedb.main:main',
        ],
    },
    author='Will Morris',
    author_email='willmorris188@gmail.com',
    description='Home Assistant Data Collection Service and Database',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/willmo103/home_assistant_litedb',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
