#boRanking

Alpha version with most useful functions implemented.

Developed by Iago Augusto Carvalho, Pedro Augusto Mendes, Tiago Costa Soares


## Overview

The project implements a bi-objective lexicographic ranking approach. The classification is done based on two input files, one containing the results of each algorithm, and the other containing the execution times for each scenario.

## Installation

Make sure you have Python 3 installed. Then, you can install the package using the following command:


import boRanking


## Usage

After installing the package.

from boRanking import biobjective_lexicographic

# Function biobjective_lexicographic:

from boRanking import biobjective_lexicographic

#Case your files have a header:
has_header = True
matrix_ranking = biobjective_lexicographic('results.csv', 'time.csv', has_header)
'Replace 'results.csv' and 'time.csv' with your file names'

#Case your files don't have a header:
matrix_ranking = biobjective_lexicographic('results.csv', 'time.csv')
'Replace 'results.csv' and 'time.csv' with your file names'
'You can define has_header as false, but not obligatory'





## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.