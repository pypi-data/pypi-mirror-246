from setuptools import setup, find_packages
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Bi-objective Lexicographical Classification'
LONG_DESCRIPTION = ('A package that allows building a matrix with the Bi-objective Lexicographical Classification '
                    'of different algorithms.')

# Setting up
setup(
    name="bi-objectiveClassification",
    version=VERSION,
    author="Iago Augusto Carvalho, Pedro Augusto Mendes, Tiago Costa Soares",
    author_email="iago.carvalho@unifal-mg.edu.br, pedroaugusto.mendes035@gmail.com, tiagocsoares22@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['csvkit'],
    keywords=['classification', 'bi-objetive', 'lexicographical', 'ranking', "csv"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    license="GPL-3.0-only"
)