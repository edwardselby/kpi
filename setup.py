"""
Setup configuration for KPI Report Generator.

Enables installation as a package with console script entry point.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="kpi-report-generator",
    version="4.0.0",
    description="Professional KPI report generator with git metrics and visualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Edward Selby",
    author_email="edward@edwardselby.com",
    url="https://github.com/edwardselby/kpi",

    #: Package discovery
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),

    #: Dependencies
    install_requires=requirements,

    #: Python version requirement
    python_requires=">=3.10",

    #: Console script entry point
    #: This creates the 'kpi' command
    entry_points={
        "console_scripts": [
            "kpi=src.main:main",
        ],
    },

    #: Package data (templates, etc.)
    package_data={
        "": ["templates/*.html"],
    },
    include_package_data=True,

    #: Classifiers for PyPI
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],

    #: Keywords
    keywords="kpi git metrics reports visualization charts matplotlib",

    #: Project URLs
    project_urls={
        "Documentation": "https://github.com/edwardselby/kpi/blob/main/README.md",
        "Source": "https://github.com/edwardselby/kpi",
        "Tracker": "https://github.com/edwardselby/kpi/issues",
    },
)
