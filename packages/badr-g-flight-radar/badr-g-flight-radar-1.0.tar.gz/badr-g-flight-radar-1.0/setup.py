from setuptools import setup, find_packages

setup(
    name="badr-g-flight-radar",  # Replace with your own package name
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    description="An ETL tool for Flight Radar data processing",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Badr_gadi/",
    author="Badr Badr",
    author_email="badr.gadi.123@gmail.com",
    install_requires=["pyspark", "FlightRadar24", "pandas", "apscheduler"],
    python_requires=">=3.6",
)
