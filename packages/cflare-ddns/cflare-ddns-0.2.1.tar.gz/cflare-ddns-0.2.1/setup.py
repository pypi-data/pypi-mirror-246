from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="cflare-ddns",
    version="0.2.1",
    author="Ian Dela Cruz",
    author_email="iandc76@gmail.com",
    url="https://github.com/ianpogi5/cflare-ddns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Yet another Cloudflare DDNS",
    packages=find_packages(),
    install_requires=["requests>=2.31.0"],
    keywords=[
        "cloudflare",
        "ddns",
        "dynamic",
        "dns",
    ],
    entry_points={
        "console_scripts": [
            "cflare-ddns=cflare_ddns.__main__:start",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: System :: Networking",
    ],
)
