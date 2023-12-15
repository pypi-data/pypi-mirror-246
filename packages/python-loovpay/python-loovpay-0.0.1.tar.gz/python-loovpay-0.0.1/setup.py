from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="python-loovpay",
    version="0.0.1",
    description="LoovPay SDK for Python",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mounir-Holding-Tech/LoovPay-Python-SDK.git",
    author="Dada Leonardo",
    author_email="dadaleonardo00@gmail.com",
    license="MIT",
    keywords=[
        "python",
        "loovpay",
        "LoovPay",
        "loov",
        "python-loovpay",
        "loovpay-python-sdk",
        "loov-solutions",
        "api-payment",
        "mobile-payment",
        "sdk",
        "payment",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests >=2.0'],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)