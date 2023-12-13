"""Building the library"""
import setuptools

setuptools.setup(
    name="tse_utils_db",
    version="1.1.6",
    author="Arka Equities & Securities",
    author_email="info@arkaequities.com",
    description="Database for Tehran Stock Exchange (TSE).",
    long_description="Database utilities for Tehran Stock Exchange, used for saving market data.",
    py_modules=["tse_market"],
    packages=["models"],
    install_requires=["python-dotenv", "SQLAlchemy", "mysql-connector-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
