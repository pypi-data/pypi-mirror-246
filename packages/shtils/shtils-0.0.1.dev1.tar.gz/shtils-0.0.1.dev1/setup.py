from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1dev1'
DESCRIPTION = 'A collection of OS shell utils'
LONG_DESCRIPTION = 'A collection of OS shell utils that allows a developer to implement often-used shell commands (like "ls" or "clear") in both Windows and Unix terms.'

# Setting up
setup(
    name="shtils",
    version=VERSION,
    author="alpenstorm (Mihai Negrean)",
    author_email="<mihai@negrean.net>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'os', 'shell', 'utils'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)