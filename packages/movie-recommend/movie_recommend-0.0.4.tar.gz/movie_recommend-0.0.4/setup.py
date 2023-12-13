from setuptools import setup, find_packages

setup(
    author='Group_7',
    description='Movie recommendation',
    name='movie_recommend',
    version='0.0.4',
    packages=find_packages(),
    package_data={
        # If any package contains *.db files, include them:
        '': ['*.db'],
    },
    include_package_data=True,
    
)