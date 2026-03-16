"""Setup script for BreathingBuddy."""

from setuptools import setup, find_packages

setup(
    name="breathingbuddy",
    version="1.0.0",
    description="Guidad andningsträning med visuella animationer",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="BreathingBuddy",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "PyGObject>=3.42",
    ],
    entry_points={
        "console_scripts": [
            "breathingbuddy=main:main",
        ],
    },
    data_files=[
        ("share/applications", ["data/com.github.breathingbuddy.desktop"]),
        ("share/locale/sv/LC_MESSAGES", ["po/sv/LC_MESSAGES/breathingbuddy.po"]),
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
)
