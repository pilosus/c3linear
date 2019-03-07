import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = "0.1.0"

setuptools.setup(
    name="c3linear",
    version=version,
    python_requires='>=3.6',
    author="Vitaly R. Samigullin",
    author_email="vrs@pilosus.org",
    description="A naive implementation of C3 linearization algorithm "
                "used in Python's MRO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pilosus/c3linear",
    download_url="https://github.com/pilosus/c3linear/archive/"
                 "{}.tar.gz".format(version),
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Education",
        "Typing :: Typed"],
    install_requires=[],
    setup_requires=[
        "pytest-runner",
        "flake8"],
    tests_require=[
        "pytest",
        "pytest-cov"],
    extras_require={
        'extra': ['mypy']},
    test_suite="tests",
)
