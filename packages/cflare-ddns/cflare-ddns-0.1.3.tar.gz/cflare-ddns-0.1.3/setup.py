from setuptools import setup, find_packages

setup(
    name="cflare-ddns",
    version="0.1.3",
    author="Ian Dela Cruz",
    author_email="iandc76@gmail.com",
    url="https://github.com/ianpogi5/cflare-ddns",
    packages=find_packages(),
    install_requires=["requests>=2.31.0"],
    entry_points={
        "console_scripts": [
            "cflare-ddns=cflare_ddns.main:main",
        ],
    },
)
