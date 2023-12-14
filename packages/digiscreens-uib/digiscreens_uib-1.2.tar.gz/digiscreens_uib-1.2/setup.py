from setuptools import setup, find_packages

setup(
    name='digiscreens_uib',
    version='1.2',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'data': ['data/*.csv', 'data/*.xlsx', 'data/scraping/*.csv']},
    install_requires=[
        'numpy',
        'pandas',
        'plotly'
    ],
    include_package_data=True,
    author='Digiscreens_team_uib',
    description='Digiscreens package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://git.app.uib.no/ii/inf219/23h/digiscreens'
)