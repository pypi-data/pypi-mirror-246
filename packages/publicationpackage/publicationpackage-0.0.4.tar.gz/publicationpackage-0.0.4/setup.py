from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'Package needed for doing a publication in Jupyter Notebook'
LONG_DESCRIPTION = 'This package contains the following functions needed to do a publication in a Jupyter Notebook: load_table_from_catalog, load_data, run_sql, write_dataframe_to_s3, get_database_info'

# Setting up
setup(
        name="publicationpackage", 
        version=VERSION,
        author="Jesse Faber",
        author_email="jesse.faber@aegon.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['boto3', 'pyspark', 'awsglue-dev'], 
        keywords=['python', 'publication', 'aws', 'pyspark', 'awsglue'],
        classifiers= [
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Framework :: Jupyter',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
        ]
)