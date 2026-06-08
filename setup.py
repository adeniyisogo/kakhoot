from setuptools import setup, find_packages

setup(
    name="kakhoot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai~=1.0",
        "anthropic~=0.20",
        "python-dotenv", # For loading API keys from .env
    ],
    entry_points={
        "console_scripts": [
            "kakhoot=kakhoot.cli:main",
        ],
    },
    author="Manus AI",
    author_email="manus@manus.im",
    description="🚀 Kakhoot: A high-performance, minimalist AI orchestration framework for building autonomous agents with plug-and-play model support.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/adeniyisogo/kakhoot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
)
