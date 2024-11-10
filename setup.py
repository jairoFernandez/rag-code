from setuptools import setup, find_packages

setup(
    name="rag-code",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[line.strip() for line in open('requirements.txt')],
    entry_points={
        "console_scripts": [
            "rag-code=rag_code_main:main",
        ],
    },
    python_requires=">=3.12",
)
