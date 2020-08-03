from setuptools import setup, find_packages

from chromepass import __version__, __author__, __email__, __license__, __title__

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", encoding='utf-8') as f:
    readme = f.read()

setup(
    name=__title__,
    version=__version__,
    description="Fetching saved passwords from chrome database file",
    long_description=readme,
    long_description_content_type='text/markdown',
    license=__license__,
    author=__author__,
    author_email=__email__,
    url="https://github.com/bierschi/chromepass",
    packages=find_packages(),
    install_requires=required,
    keywords=["chrome", "passwords", "database", "browser", "windows", "linux"],
    python_requires=">=3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={
        "console_scripts": [
            'chromepass = chromepass.main:main'
        ],
    },
    zip_safe=False,
)
