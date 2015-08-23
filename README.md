# Name

csvMagic

# Version

alpha 0.1 (released 2015-08-23)

# Author

- Martin Larsson
	- E-mail: [to.martin.larsson@gmail.com](to.martin.larsson@gmail.com)
	- Homepage: [www.martinlarsson.net](www.martinlarsson.net)

# License type

GNU Gen­eral Public Li­cense, ver­sion 3

# Description

csvMagic is a program that modifies csv files for you in accordance with certain criterias. More specifically, you supply the program with a data file and a modify file. The program then goes through the modify file and changes all dthe ata cells of the input file in accordence with a certain rule set.

# Dependencies

In order to run this program, you need [Python](https://www.python.org/) installed and ready to go.

# Basic usage

You run the program by typing

	python csvMagic InputFile ModifyFile OutputFile Delimiter

with all the files you want to use placed in the same directory as `csvMagic.py`. Here, `InputFile` refers to your master data file. This has to be a `csv` file with a header row specifying the column names and at least one row of data after that. `ModifyFile` refers to your modify file. This also has to be a `csv` file with a header row specifying the column names and at least one row of data after that. `OutputFile` refers to the file  that you want the output to be written to. If this file already exists, it will be overwritten. If it doesn't exists, it will be created. `Delimiter` refers to the delimiter character that is, and should be used, in the csv data. This character should be given within quotation marks.

In your modify file, you mark the columns that you want the program to look at by a letter and then the `@` symbol, followed by the column name in the input file. Currently, there are two commands that you can use:

- `v@` - **Vertabim check:** Makes the program check to see if the cells in this column match with the cells in the input file.
- `c@` - **Change:** Tells the program that these are the columns that you want to change if it finds a match.

The program will, for each row in the modify file, first look at all the `v@` tags. If all the cells in a row of the modify file where the column name is marked with `v@` match with all the cells for those column names in the input data, the program will look in the modify file for columns tagged with `c@`. For all these, the content of the cells in the modify will replace whatever is present in the input file.

# Change log

## alpha 0.1 (released 2015-08-23)
- Added the most basic funcionality: Look for matching rows between the modify and the input files and create an output file where the 
