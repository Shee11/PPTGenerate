from setuptools import setup, find_packages

setup(
    name="uce-render",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0,<3.0",
        "jinja2>=3.1,<4.0",
        "click>=8.0,<9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0,<8.0",
            "pytest-cov>=4.0,<5.0",
            "ruff>=0.1.0",
            "mypy>=1.7",
        ],
    },
    entry_points={
        "console_scripts": [
            "uce-render=cli.uce_render:cli",
        ],
    },
    python_requires=">=3.11",
)
