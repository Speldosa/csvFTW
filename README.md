# Name

csvFTW

# Version

alpha 0.5 (released 2015-10-13)

# Author

- Martin Larsson
	- E-mail: [to.martin.larsson@gmail.com](to.martin.larsson@gmail.com)
	- Homepage: [www.martinlarsson.net](http://www.martinlarsson.net)

# License type

GNU Gen­eral Public Li­cense, ver­sion 3

# Description

csvFTW is a program that modifies csv files for you in accordance with certain criterias. More specifically, you supply the program with a data file and a modify file. The program then goes through the modify file and changes all dthe ata cells of the input file in accordence with a certain rule set.

# Dependencies

In order to run this program, you need [Python](https://www.python.org/) installed and ready to go.

# Basic usage

You run the program by typing

	python csvFTW.py mode inputFile instructionFile outputFile delimiter

with all the files you want to use placed in the same directory as `csvFTW.py`. Here, `mode`refers to one of the two modes the program can be set to: `remove` or `modify`. `inputFile` refers to your master data file. This has to be a `csv` file with a header row specifying the column names and at least one row of data after that. `instructionFile` refers to your instruction file. This also has to be a `csv` file with a header row specifying the column names and at least one row of data after that. `outputFile` refers to the file  that you want the output to be written to. If this file already exists, it will be overwritten. If it doesn't exists, it will be created. `delimiter` refers to the delimiter character that is, and should be used, in the csv data. This character should be given within quotation marks.

In your instruction file, you mark the columns that you want the program to look at by a letter and then the `@` symbol, followed by the column name in the input file. Currently, there are two commands that you can useto define checks:

- `v@` - **Vertabim check:** Makes the program check to see if the cells in this column match with the cells in the input file.
- `w@` - **Words check:** Makes the program check to see if the cells in this column match with the cells in the input file. This markup uses a special markup to look for different vertabim matches in one fell swoop. Elements are separated by `+`, like so: `x+y`. Here, both `x` and `y` would be considered matches if it shows up in the input data. Notice however that plusses cannot be part of the content being matched in the input data.
- `i@` - **Integer check:** Makes the program check to see if the cells in this column match with the cells in the input file. This markup only deals with integers and a special syntax can be used to look for several of them in one fell swoop. First, elements can be separated by commas, like so: `x,y`. Further, each element can be a range between two numbers (with the smaller one specified first). For example, `1-5` would be the same thing as writing `1,2,3,4,5`. An example of a integer check could then be `1-3,5-8,10` which would match with all numbers between 1 and 10 except for 4 and 9. In addition, using a `*` (not applicable in the range option) means that any number passes.

Depending on the mode the program is run in, it will behave in different ways:

## Remove mode

In this mode, the program will, for each row in the instruction file, look at all the `v@`, `w@`, and `i@` tags. If all the cells in a row of the instruction file where the column name is marked with `v@`, `w@`, or `i@` match with all the cells for those column names in one or several rows of the input data, the program will remove these rows from the input data.

## Modify mode

The program will, for each row in the instruction file, first look at all the `v@`, `w@`, and `i@` tags. If all the cells in a row of the instruction file where the column name is marked with `v@`, `w@`, or `i@` match with all the cells for those column names in one or several rows of the input data, the program will look in the instruction file again for columns tagged with `m@` (which stands for `modify`). For all these, the content of the cells in the instruction file will replace whatever is present in the input file for the output data, or add a new column with the name specified after the `@` sign.


# Change log

## alpha 0.6 (released 2015-11-03)
- Added a new markup: `w@` (words).

## alpha 0.5 (released 2015-10-13)
- Added the mode option so that the program can be run in two different modes: `remove` and `modify`.

## alpha 0.4 (released 2015-10-05)
- Fixed some bugs.

## alpha 0.3 (released 2015-09-08)
- Changed the name from `csvMagic` to `csvFTW`.
- Added the star option to `i@` (integer).
- Fixed some bugs.

## alpha 0.2 (released 2015-08-29)
- Changed the `c@` (change) syntax to `m@` (modify).
- Added a new markup: `i@` (integer).
- Made it so that column names specified in the modify file that doesn't exist in the input data are created for the output.
- Added several FYI (for your information) and result messages that are printed to the terminal to better help the user understand what the program is doing and what things one possibly might want to fix in the data.
- Cleaned up some of the code.

## alpha 0.1 (released 2015-08-23)
- Added the most basic funcionality: Look for matching rows between the modify and the input files and create an output file where the 
