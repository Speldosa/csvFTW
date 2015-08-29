########################
## 1. Import packages ##
########################

# The csv package is necessary to handle csv files.
import csv
# The sys package enables one to abort a program with some kind of error message.
import sys


#############################
## 2. Function definitions ##
#############################

def check_for_match(modify_row,modify_column,check_column_name,check_column_markup,input_row, data):
	if check_column_markup == 'v@':
		for a in range(0,len(data.input_data_header_columns)):
			if check_column_name == data.input_data_header_columns[a]:
				if data.modify_data[modify_row][modify_column]:
					if data.modify_data[modify_row][modify_column] == data.input_data[input_row][a]:
						return(True)
					elif data.modify_data[modify_row][modify_column] == rules.empty_designator:
						if data.input_data[input_row][a] == "":
							return(True)
		return(False)
	elif check_column_markup == 'i@':
		currentCell = data.modify_data[modify_row][modify_column]
		if ',' in currentCell:
			currentCellElements = currentCell.split(",")
			for a in range(0,len(currentCellElements)):
				currentCellElements[a].replace(" ", "")
		else:
			currentCellElements = [currentCell]
		for a in range(0,len(data.input_data_header_columns)):
			if check_column_name == data.input_data_header_columns[a]:
				for b in range(0,len(currentCellElements)):
					if currentCellElements[b]:
						if currentCellElements[b] == data.input_data[input_row][a]:
							return(True)
						elif "-" in currentCellElements[b]:
							current_cell_element_range = currentCellElements[b].split("-")
							if len(current_cell_element_range) == 2:
								try:
									if int(current_cell_element_range[0]) < int(current_cell_element_range[1]):
										for c in range(int(current_cell_element_range[0]),int(current_cell_element_range[1])):
											if c == int(data.input_data[input_row][a]):
												return(True)
								except:
									# To-do: Catch this error in the check construct.
									pass
						elif data.modify_data[modify_row][modify_column] == rules.empty_designator:
							if data.input_data[input_row][a] == "":
								return(True)
		return(False)
	raise Exception('No known markup.')

def list_key_columns(list_of_column_names, key_string, data):
	white_list = []
	for a in range(0, len(list_of_column_names)):
		current_cell = data[0][a]
		if len(current_cell) >= len(key_string):
			if current_cell[:len(key_string)] == key_string:
				white_list.append(a)
	return(white_list)

def create_number_list(input):
	output_list = []
	for a in range(0,len(input)):
		output_list.append(a)
	return(output_list)

def print_ignored_columns_message(data):
	if data.modify_data_non_marked_columns:
		Message_to_print=""
		Message_to_print+="FYI: The following columns were not marked up in the modify file and will therefore be ignored: "
		for a in data.modify_data_non_marked_columns:
			Message_to_print+="\"" + data.modify_data[0][a] + "\", "
		Message_to_print=Message_to_print[:len(Message_to_print)-2]
		print(Message_to_print)

def print_startup_message(data,rules):
	print("************************************")
	print("*** csvmagic, alpha version 0.2. ***")
	print("************************************")
	print("Input file: " + data.input_file)
	print("Modify file: " + data.modify_file)
	print("Output file: " + data.output_file)
	print("Delimiter: " + rules.delimiter)

def print_new_columns_created(checks):
	if checks.new_columns_created:
		Message_to_print=""
		Message_to_print+="FYI: The following columns were not found in the input data and were therefore created: "
		for a in range(0,len(checks.new_columns_created)):
			Message_to_print+="\"" + checks.new_columns_created[a] + "\", "
		Message_to_print=Message_to_print[:len(Message_to_print)-2]
		print(Message_to_print)

def print_unaffective_mofify_rows(checks):
	if checks.unaffective_modify_rows:
		Message_to_print=""
		Message_to_print+="FYI: The following rows in the modfify file didn't match with any rows in the input data: "
		for a in range(0,len(checks.unaffective_modify_rows)):
			Message_to_print+=str(checks.unaffective_modify_rows[a]+1) + ", "
		Message_to_print=Message_to_print[:len(Message_to_print)-2]
		print(Message_to_print)

def print_several_modifications(checks):
	message_to_print=""
	any_hit_yet = False
	for a in range(0,len(checks.multiple_modifications[2])):
		if len(checks.multiple_modifications[2][a]) > 1:
			if not any_hit_yet:
				message_to_print += "WARNING: The following cells in the output data have been maniupulated several times by the modify data (where the highest numbered modify row decides the output value of the cell): "
			any_hit_yet = True
			message_to_print += "\n	Output row/column " + str(checks.multiple_modifications[0][a] + 1) + "/" + str(checks.multiple_modifications[1][a] + 1) + " has been manipulated by the following modify rows: "
			for b in range(0,len(checks.multiple_modifications[2][a])):
				message_to_print+=str(checks.multiple_modifications[2][a][b] + 1) + ", "
			message_to_print=message_to_print[:len(message_to_print)-2]
	if message_to_print != "":
		print(message_to_print)

def print_non_existent_check_columns(data):
	if data.non_existent_check_columns:
		message_to_print=""
		message_to_print+="FYI: The following columns were marked for checking in the modify data but had no matches in the input data: "
		for a in range(0,len(data.non_existent_check_columns)):
			message_to_print+="\"" + data.non_existent_check_columns[a] + "\", "
			message_to_print=message_to_print[:len(message_to_print)-2]
		print(message_to_print)

##########################
## 3. Class definitions ##
##########################

### Rules ###
class Rules:
	def __init__(self,delimiter,key_designator_lenght,empty_designator):
		self.delimiter = delimiter
		self.key_designator_lenght = key_designator_lenght
		self.empty_designator = empty_designator

### Data ###
class Data:
	def __init__(self,input_file,modify_file,output_file,rules):
		self.input_file = input_file
		self.modify_file = modify_file
		self.output_file = output_file
		# Import Input data.
		with open(self.input_file, 'r') as csvfile:
			self.input_data = list(csv.reader(csvfile, delimiter=rules.delimiter))
			self.input_data_header_columns = self.input_data[0]

		# Import Modify data.
		with open(self.modify_file, 'r') as csvfile:
			self.modify_data = list(csv.reader(csvfile, delimiter=rules.delimiter))
			self.modify_data_header_columns = self.modify_data[0]

		# Import Output data.
		self.output_data = self.input_data
		self.output_data_header_columns = self.input_data_header_columns

		# Create variables
		self.modify_data_vertabim_columns = list_key_columns(self.modify_data_header_columns, "v@", self.modify_data)
		self.modify_data_integer_columns = list_key_columns(self.modify_data_header_columns, "i@", self.modify_data)
		self.modify_data_check_columns = self.modify_data_vertabim_columns + self.modify_data_integer_columns
		self.modify_data_change_columns = list_key_columns(self.modify_data_header_columns, "m@", self.modify_data)
		self.modify_data_marked_columns = self.modify_data_check_columns + self.modify_data_change_columns
		self.modify_data_all_columns = create_number_list(self.modify_data_header_columns)
		self.modify_data_non_marked_columns = [item for item in self.modify_data_all_columns if item not in self.modify_data_marked_columns]

		# Make a list of all check columns that haven't got a correspondence in the input file. Remove these from the check columns.
		self.non_existent_check_columns = []
		self.modify_data_check_columns_actual = []
		for a in range(0,len(self.modify_data_check_columns)):
			current_column_name = self.modify_data[0][self.modify_data_check_columns[a]]
			current_column_name_without_markup = current_column_name[rules.key_designator_lenght:]
			if current_column_name_without_markup not in self.input_data_header_columns:
				self.non_existent_check_columns.append(current_column_name)
			else:
				self.modify_data_check_columns_actual.append(self.modify_data_check_columns[a])
		self.modify_data_check_columns = self.modify_data_check_columns_actual


	def modify_output(self,input_row,modify_row,rules,checks):
		for a in range(0,len(self.modify_data_change_columns)):
			if self.modify_data[modify_row][self.modify_data_change_columns[a]]:
				change_column_name = self.modify_data[0][self.modify_data_change_columns[a]]
				change_column_markup = change_column_name[:rules.key_designator_lenght]
				change_column_name = change_column_name[2:]
				column_already_exists = False
				if not change_column_name in self.output_data_header_columns:
					self.add_new_column(change_column_name)
				self.output_data[input_row][self.output_data[0].index(change_column_name)] = self.modify_data[modify_row][self.modify_data_change_columns[a]]
				checks.output_modified(input_row,self.output_data[0].index(change_column_name),modify_row,self)

	def add_new_column(self,new_column_name):
		self.output_data[0].append(new_column_name)
		checks.new_column_created(new_column_name)
		for a in range(1,len(self.output_data)):
			self.output_data[a].append("")
		return(input)

### Checks ###
class Checks:
	new_columns_created = []
	unaffective_modify_rows = []
	multiple_modifications = [[],[],[]]

	def new_column_created(self,new_column_name):
		self.new_columns_created.append(new_column_name)

	def output_modified(self,output_row,output_column,modify_row,data):
		found_an_output_hit = False
		found_a_modify_hit = False
		for a in range(0,len(self.multiple_modifications[0])):
			if self.multiple_modifications[0][a] == output_row:
				if self.multiple_modifications[1][a] == output_column:
					found_an_output_hit = True
					write_to_row = a
					try:
						if modify_row in self.multiple_modifications[2][a]:
							found_a_modify_hit = True
					except:
						pass
		if not found_an_output_hit:
			self.multiple_modifications[0].append(output_row)
			self.multiple_modifications[1].append(output_column)
			self.multiple_modifications[2].append([modify_row])
		else:
			if not found_a_modify_hit:
				self.multiple_modifications[2][write_to_row].append(modify_row)
						
### Session ###
class Session:
	def test():
		print("Session.test()")
		
#############################
## 3. Object instantiation ##
#############################

rules = Rules(sys.argv[4],2,"<empty>")
data = Data(sys.argv[1],sys.argv[2],sys.argv[3],rules)
checks = Checks()
session = Session()


####################
## 4. Run program ##
####################

# Print startup messages.
print("")
print_startup_message(data,rules)

for a in range(1,len(data.modify_data)):
	modify_at_least_one_hit_for_modify_row = False
	for b in range(1,len(data.input_data)):
		for c in range(0,len(data.modify_data_check_columns)):
			check_column_number = data.modify_data_check_columns[c]
			check_column_name = data.modify_data[0][check_column_number]
			check_column_markup = check_column_name[:rules.key_designator_lenght]
			check_column_name = check_column_name[rules.key_designator_lenght:]
			if check_for_match(a,data.modify_data_check_columns[c],check_column_name,check_column_markup,b,data):
				if c == (len(data.modify_data_check_columns) - 1):
					modify_at_least_one_hit_for_modify_row = True
					data.modify_output(b,a,rules,checks)
			else:
				break
	if not modify_at_least_one_hit_for_modify_row:
		checks.unaffective_modify_rows.append(a)

# Print closedown messages.
print("")
print_non_existent_check_columns(data)
print_ignored_columns_message(data)
print_new_columns_created(checks)
print_unaffective_mofify_rows(checks)
print_several_modifications(checks)
print("")

# Write Output to file
with open(data.output_file, 'w') as file:
	File_writer = csv.writer(file, delimiter=rules.delimiter, quoting=csv.QUOTE_ALL)
	File_writer.writerows(data.output_data)