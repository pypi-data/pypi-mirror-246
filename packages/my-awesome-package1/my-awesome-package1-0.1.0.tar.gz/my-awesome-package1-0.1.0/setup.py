from setuptools import setup, find_packages

setup(
    name="my-awesome-package1",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 在这里列出你的库所需的其他Python包
    ],

    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your awesome package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/fansxs/my-awesome-package1",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)