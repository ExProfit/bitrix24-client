from setuptools import setup, find_packages

setup(
    name="bitrix24-client",
    version="0.1.0",
    packages=find_packages(),
    url="https://github.com/exprofit/bitrix24-client",
    install_requires=[
        "httpx>=0.28.1",
        "pydantic>=2.12.5",
        "loguru>=0.7.3",
    ],
    python_requires=">=3.12",
)