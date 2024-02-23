from setuptools import setup

setup(
    name="content", 
    description="cONTent is a tool-box allowing the analysis of ONT long-reads length and quality.", 
    packages=["content"], 
    entry_points={"console_scripts": ["content=content.main:main"]}
)

