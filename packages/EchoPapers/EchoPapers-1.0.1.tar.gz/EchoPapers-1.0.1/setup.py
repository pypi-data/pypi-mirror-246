from setuptools import setup, find_packages
import re

version = None
for line in open("./EchoPapers/__init__.py"):
    m = re.search("__version__\s*=\s*(.*)", line)
    if m:
        version = m.group(1).strip()[1:-1]  # quotes
        break
assert version

setup(
    name='EchoPapers',
    version=version,
    packages=["EchoPapers"],
    package_data={"": ["README.md"]},
    python_requires='>=3.6',
    include_package_data=True,
    scripts=[
        'EchoPapers/scholar_scraper.py',
        'EchoPapers/scholar_parser.py',
        'EchoPapers/scholar_citing.py'
    ],
    license="MIT",
    url='https://github.com/ad3002/EchoPapers',
    author='Aleksey Komissarov',
    author_email='ad3002@gmail.com',
    description='EchoPapers: Discover and analyze the impact of academic papers through citation tracking and advanced analytics',
    install_requires=[
        'EchoReaper',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)
