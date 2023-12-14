from setuptools import setup, find_packages

setup(
    name='obsidian_linker',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'openai',
        'python-dotenv',
    ],
    entry_points='''
        [console_scripts]
        obsidian_linker=obsidian_linker.main:main
    ''',
)