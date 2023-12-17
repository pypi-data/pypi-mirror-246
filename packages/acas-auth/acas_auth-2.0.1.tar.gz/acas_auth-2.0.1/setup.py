from setuptools import setup, find_packages

setup(
    name='acas_auth',
    version='2.0.1',
    packages=find_packages(),
    install_requires=[
        "Flask==3.0.0",
        "Flask-Bcrypt==1.0.1",
        "Flask-Login==0.6.3",
        "Flask-Mail==0.9.1",
        "Flask-Migrate==4.0.5"
    ]
)
