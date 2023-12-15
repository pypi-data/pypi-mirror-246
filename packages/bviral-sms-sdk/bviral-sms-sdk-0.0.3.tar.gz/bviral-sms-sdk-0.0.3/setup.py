from setuptools import setup, find_packages

setup(
    name="bviral-sms-sdk",
    version="0.0.3",
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
        "pydantic>=2.4.2",
        "requests>=2.24.0",
        "dataclasses-json>=0.6.0",
    ],
    zip_safe=False,
)