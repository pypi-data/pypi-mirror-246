from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

#with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Emoji converter from text'
LONG_DESCRIPTION = 'A package that allows to convert a text with emojies into their corresponding meaning to allow NLP language models to help interpret them easier'

# Setting up
setup(
    name="gmoji",
    version=VERSION,
    author="Ganesh PS",
    author_email="<ganeshps97@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=['python', 'NLP', 'emoji converter', 'emoji meaning', 'emoji to text'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
