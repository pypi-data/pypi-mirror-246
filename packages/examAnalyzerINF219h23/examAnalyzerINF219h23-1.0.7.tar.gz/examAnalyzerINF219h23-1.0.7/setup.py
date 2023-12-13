from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.7'
DESCRIPTION = 'Exam analyzer is a tool that extract data from Json files from Inspera, and then creates visualizations with descriptive texts'

# Setting up
setup(
    name="examAnalyzerINF219h23",
    version=VERSION,
    author="Tobias, Jonas, Brage, Prem",
    author_email="premeide@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    package_data={'examAnalyzerINF219h23': ['templates/*']},
    install_requires=['Flask'],
    keywords=['python', 'education', 'exam analysis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
