from setuptools import setup, find_packages

setup(
    name="bitrix24-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.28.0",
        "pydantic>=2.12.0",
        "loguru>=0.7.0",
    ],
    python_requires=">=3.9",
)