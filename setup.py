from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rentry",
    version="0.1.0",
    author="Contributor",
    author_email="email@example.com",
    description="Command line client for rentry.co",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spignelon/rentry",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
    ],
    entry_points={
        'console_scripts': [
            'rentry=rentry.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
