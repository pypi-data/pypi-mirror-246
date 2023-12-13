
from setuptools import setup, find_packages

setup(
    author='Mane Davtyan',
    description='BookStore Recommendation System',
    name='bookrecs',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'Faker==20.1.0',
        'fastapi==0.105.0',
        'numpy==1.24.4',
        'pandas==2.0.3',
        'pydantic==2.5.2',
        'scikit-learn==1.3.2',
        'setuptools==65.5.1',
        'setuptools==65.5.1',
        'SQLAlchemy==2.0.23',
        'uvicorn==0.24.0.post1',
    ],
)
