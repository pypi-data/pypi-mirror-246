from setuptools import setup, find_packages

setup(
    name="devrevteamthirtyone",
    version="0.2.0",
    author="Team31",
    author_email="team31-interiit@gmail.com",
    description="Submission for team31",
    long_description="This takes tools and queries and returns a solution",
    packages=find_packages(),
    install_requires=["tiktoken", "litellm", "numpy"]
)