from io import open

from setuptools import setup


setup(
    # ? Genel Bilgiler
    name="aylak",
    version="0.0.2.1",
    url="https://github.com/aylak-github/aylak-pypi",
    description="Aylak PyPi",
    keywords=["aylak", "pypi", "aylak-pypi", "aylak-pypi"],
    author="aylak-github",
    author_email="contact@yakupkaya.net.tr",
    license="GNU AFFERO GENERAL PUBLIC LICENSE (v3)",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
    ],
    # ? Paket Bilgileri
    packages=["aylak"],
    python_requires=">=3.10",
    install_requires=[
        "setuptools",
        "wheel",
        "Pillow",
        "pythonansi",
        "poetry-core>=1.0.0",
    ],
    # ? PyPI Bilgileri
    long_description_content_type="text/markdown",
    include_package_data=True,
)
