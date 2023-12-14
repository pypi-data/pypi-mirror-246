from setuptools import setup, find_packages

# Setting up
setup(
    name="py-frameless-utils",
    version="0.1.3",
    author="KE",
    author_email="",
    description="Various utilities not depending on Flask/FastAPI or other framework",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["PyJWT==2.8.0"],
    keywords=["python", "decorator", "token"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
)
