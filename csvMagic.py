########################
## 1. Import packages ##
########################
# The csv package is necessary to handle csv files.
import csv
# The sys package enables one to abort a program with some kind of error message.
import sys

###################################################
## 2. Globabl variables and function definitions ##
###################################################

# Global variables
KeyDesignatorLenght = 2
emptyDesignator = "<empty>"

# function: listKeyColumns
# description: -
def listKeyColumns(ListOfColumnNames, KeyString):
	WhiteList = []
	for a in range(0, len(ListOfColumnNames)):
		CurrentCell = Modify[0][a]
		if len(CurrentCell) >= len(KeyString):
			if CurrentCell[:len(KeyString)] == KeyString:
				WhiteList.append(a)
	return(WhiteList)

# function: createNumberList
# description: -
def createNumberList(Input):
	outputList = []
	for a in range(0,len(Input)):
		outputList.append(a)
	return(outputList)

# function: checkForMatch
# description: -
# EXPAND THIS FUNCTION TO ACCOMODATE DIFFERT MARKUPS. RIGHT NOW, IT ASSUMES v@.
def checkForMatch(Modify,ModifyRow,ModifyColumn,CheckColumnName,CheckColumnMarkup,Input,InputRow):
	Input_HeaderColumns = Input[0]
	Modify_HeaderColumns = Modify[0]
	for a in range(0,len(Input_HeaderColumns)):
		if CheckColumnName == Input_HeaderColumns[a]:
			if Modify[ModifyRow][ModifyColumn]:
				if Modify[ModifyRow][ModifyColumn] == Input[InputRow][a]:
					return(True)
				elif Modify[ModifyRow][ModifyColumn] == emptyDesignator:
					if Input[InputRow][a] == "":
						return(True)
	return(False)

# function: modifyOutput
# description: -
def modifyOutput(Modify,UseModifyRow,ChangeColumns,Output,ChangeOutputRow):
	Output_HeaderColumns = Output[0]
	for a in range(0,len(ChangeColumns)):
		if Modify[UseModifyRow][ChangeColumns[a]]:
			ChangeColumnName = Modify[0][ChangeColumns[a]]
			ChangeColumnMarkup = ChangeColumnName[:KeyDesignatorLenght]
			ChangeColumnName = ChangeColumnName[2:]
			Output_HeaderColumns = Output[0]
			for b in range(0,len(Output_HeaderColumns)):
				if ChangeColumnName == Output_HeaderColumns[b]:
					Output[ChangeOutputRow][b] = Modify[UseModifyRow][ChangeColumns[a]]
					break
	return(Output)

###############################
## 3. Print startup messages ##
###############################
print("\n************************************")
print("*** csvmagic, alpha version 0.1. ***")
print("************************************")
print("Input file: " + sys.argv[1])
print("Modify file: " + sys.argv[2])
print("Output file: " + sys.argv[3])
print("Delimiter: " + sys.argv[4])
print("")

####################
## 4. Import data ##
####################
Input_File = sys.argv[1]
Modify_File = sys.argv[2]
Output_File = sys.argv[3]
Delimiter = sys.argv[4]

# Import Input data.
with open(Input_File, 'r') as csvfile:
	Input = list(csv.reader(csvfile, delimiter=Delimiter))
Input_HeaderColumns = Input[0]

# Import Modify data.
with open(Modify_File, 'r') as csvfile:
	Modify = list(csv.reader(csvfile, delimiter=Delimiter))
Modify_HeaderColumns = Modify[0]

# Import Output data.
Output = Input
Output_HeaderColumns = Input_HeaderColumns

####################
## 5. Run program ##
####################
CheckColumns = listKeyColumns(Modify_HeaderColumns, "v@") + listKeyColumns(Modify_HeaderColumns, "i@")
ChangeColumns = listKeyColumns(Modify_HeaderColumns, "c@")
MarkedColumns = CheckColumns + ChangeColumns
AllColumns = createNumberList(Modify_HeaderColumns)
NonMarkedColumns = [item for item in AllColumns if item not in MarkedColumns]
if NonMarkedColumns:
	for a in NonMarkedColumns:
		print("WARNING: Modify column " + str(a+1) + " (\"" + Modify[0][a] + "\") hasn't been marked up. Column will be ignored.")

# CREATE A FUNCTION FOR CHECKING IF THE DATA ALREADY HAS BEEN MODIFIED BY ANOTHER MODIFY ROW.
# Output_DataAlreadyModified = []

for a in range(1,len(Modify)):
	Modify_atLeastOneHitForModifyRow = False
	for b in range(1,len(Input)):
		for c in range(0,len(CheckColumns)):
			CheckColumnNumber = CheckColumns[c]
			CheckColumnName = Modify[0][CheckColumnNumber]
			CheckColumnMarkup = CheckColumnName[:KeyDesignatorLenght]
			CheckColumnName = CheckColumnName[KeyDesignatorLenght:]
			if checkForMatch(Modify,a,CheckColumns[c],CheckColumnName,CheckColumnMarkup,Input,b):
				if c == (len(CheckColumns) - 1):
					Modify_atLeastOneHitForModifyRow = True
					Output = modifyOutput(Modify,a,ChangeColumns,Output,b)
			else:
				break
	if not Modify_atLeastOneHitForModifyRow:
		print("FYI: Modify row number " + str(b) + " doesn't match with any data row and is therefore not modifying anything.")

with open(Output_File, 'w') as file:
	FileWriter = csv.writer(file, delimiter=Delimiter, quoting=csv.QUOTE_ALL)
	FileWriter.writerows(Output)

# Print the variable Output to file:


#################################
## 6. Print closedown messages ##
#################################
print("")