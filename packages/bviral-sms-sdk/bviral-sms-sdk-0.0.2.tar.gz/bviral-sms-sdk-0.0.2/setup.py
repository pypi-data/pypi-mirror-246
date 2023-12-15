from setuptools import setup, find_packages

setup(
    name="bviral-sms-sdk",
    version="0.0.2",
    description="A Python wrapper around for Social Media Data API.",
    author="Cherif Mohamed Yassine",
    author_email="senpaireymes@gmail.com",
    license="MIT",
    keywords=["sms-api", "sms-sdk"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    packages=find_packages(),
    install_requires=[
        "pydantic>=22.4.2",
        "requests>=2.24.0",
        "dataclasses-json>=0.5.3; python_version<'3.7'",
        "dataclasses-json>=0.6.0; python_version>='3.7'",
    ],
    extras_require={
        "dev": [
            "responses>=0.17.0; python_version<'3.7'",
            "responses>=0.23.0; python_version>='3.7'",
            "pytest>=6.2; python_version<'3.7'",
            "pytest>=7.1; python_version>='3.7'",
            "pytest-cov>=2.10.1; python_version<'3.7'",
            "pytest-cov>=3.0.0; python_version>='3.7'",
        ]
    },
    zip_safe=False,
)