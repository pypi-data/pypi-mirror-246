import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hivepepebot",
    version="0.0.1",
    author="Erik Gustafsson and Hive Pizza Team",
    author_email="erikegse@gmail.com",
    description="A script to find and react to !PEPE commands in comments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flaxz/hivepepebot",
    project_urls={
        "Bug Tracker": "https://github.com/flaxz/hivepepebot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
    zip_safe=False,
)