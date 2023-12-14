import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PKG_NAME = "Netzwerk_pkg"
USER_NAME = "palasanimahesh46"
PROJECT_NAME = "Netzwerk_pkg"

setuptools.setup(
    name=f"{PKG_NAME}-{USER_NAME}",
    version="0.0.3",
    author=USER_NAME,
    author_email="palasanimahesh46@gmail.com",
    description="A small package for perceptron",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{USER_NAME}/{PROJECT_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{USER_NAME}/{PROJECT_NAME}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "numpy==1.24.3",
        "pandas==2.0.3",
        "joblib==1.1.1"
    ]
)