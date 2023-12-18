from setuptools import setup, find_packages

setup(
    name="Spectralanalysis",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for spectral analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Spectralanalysis",  # Use the URL to the github repo or website
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas",
        "scikit-learn",
        "numpy",
        "scipy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
