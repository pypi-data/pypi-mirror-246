from skbuild import setup  # This line replaces 'from setuptools import setup'

setup(
    name="aalink",
    version="0.0.6",
    description="Async Python interface for Ableton Link",
    author="Artem Popov",
    license="GPL",
    packages=["aalink"],
    python_requires=">=3.8",
)
