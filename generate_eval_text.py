# This class searches the given student's eval file
# and appends the given line to the given tag

import os, sys
from collections import OrderedDict

if (len(sys.argv) < 2):
	target = raw_input("Evergreen Login? ")
else:
	target = sys.argv[1]

override = None

if (len(sys.argv) >= 3):
	override = sys.argv[2]

if (override != None):
	print("Override detected")

repos_dir = "repos"

def build_filename(dir, suffix):
	return repos_dir + "/" + target + "/" + dir + "/" + target + "-" + suffix + ".txt"

sem_in_filename = build_filename("sem", "eval")
sem_out_filename = build_filename("sem", "words")
sem_cred_filename = build_filename("sem", "credits")
prog_in_filename = build_filename("prog", "eval")
prog_custom_filename = build_filename("prog", "custom")
prog_out_filename = build_filename("prog", "words")
prog_cred_filename = build_filename("prog", "credits")

import names
gender_dict = names.student_info_dict("email", "gender")
gender = gender_dict[target]
name_dict = names.student_info_dict("email", "preferred_name")
name = name_dict[target]

def close_file(in_file, out_file, cred_file):
	in_file.close()
	out_file.close()
	cred_file.close()

def open_or_create_file(filename, test_mode, final_mode):
	try:
		infile = open(filename, test_mode)
	except IOError, (ErrorNumber, ErrorMessage):
		if ErrorNumber == 2: # file not found
			print("Creating " + in_filename + " because it does not exist")
			infile = open(in_filename, final_mode)
			infile.writelines([])
			infile.close()
			infile = open(in_filename, final_mode)
	return infile
	

def open_file(in_filename, out_filename, cred_filename):
	infile = None
	outfile = None
	credfile = None

	infile = open_or_create_file(in_filename, "r", "r")
	outfile = open_or_create_file(out_filename, "w", "w")
	credfile = open_or_create_file(cred_filename, "w", "w")

	return (infile, outfile, credfile)

(sem_in_file, sem_out_file, sem_cred_file) = open_file(sem_in_filename, sem_out_filename, sem_cred_filename)
if (sem_out_file == None):
	exit
(prog_in_file, prog_out_file, prog_cred_file) = open_file(prog_in_filename, prog_out_filename, prog_cred_filename)
prog_custom_file = None
try:
	prog_custom_file = open(prog_custom_filename)
except IOError:
	print("No custom file found")


def generate_eval_text(infile, outfile, credfile, callback_func_list):

	lines = infile.readlines()

	tags = set(lines)
	tags -= set(['\n'])

	for func in callback_func_list:
		(text_lines, cred_lines) = func(tags)
		outfile.writelines(text_lines)
		credfile.writelines(cred_lines)


def sem_callback(tags):
	sem_count = 0

	import re

	text_lines = []
	cred_lines = []

	for x in tags:
		tokens = x.split(":")
		results = re.search("\{S[0-9]*\}", tokens[0])
		if (results != None):
			sem_count += 1

	if (sem_count >= 4):
		text_lines.append(name + ' attended ' + str(sem_count) + ' out of 10 seminars, participated well in discussion, and wrote response papers to the speaker series.\n\n')
		credit_num = 1
		if (sem_count >= 8):
			credit_num = 2
		cred_lines.append(str(credit_num) + ' - Seminar on PLATO Lecture Series: Greeners on the Cutting Edge\n')

	return (text_lines, cred_lines)

def talk_callback(tags):
	talk_count = 0

	import re

	text_lines = []
	cred_lines = []

	for x in tags:
		tokens = x.split(":")
		results = re.search("\{SS[0-9]*\}", tokens[0])
		if (results != None):
			talk_count += 1

	if (talk_count >= 3):
		credit_num = 1
		if (talk_count >= 7):
			credit_num = 2
		text_lines += name + ' attended ' + str(talk_count) + ' out of 9 talks of the PLATO Lecture Series.\n\n'
		cred_lines += str(credit_num) + ' - PLATO Lecture Series: Greeners on the Cutting Edge\n'

	return (text_lines, cred_lines)

def prog_callback(tags):

	import re

	text_lines = []
	cred_lines = []

	ijava_dict = OrderedDict([
		("{C1}" , "basic Java syntax"),
		("{C2}" , "basic Java objects and classes"),
		("{C3}" , "the import statement and input Scanner"),
		("{C4}" , "loop and conditional statements"),
		("{C5}" , "declaring and calling methods"),
		("{C6}" , "autoboxing primitive types to reference types and graphical input/output"),
		("{C7}" , "arrays"),
		("{C8}" , "programs of up to 100 lines in size"),
		("{C9}" , "inheritance")
	])	

	prog_count = 0
	for x in tags:
		tokens = x.split(":")
		tag = tokens[0].rstrip()
		results = re.search("\{C[0-9]*\}", tag)
		if (results != None):
			print("Detected tag" + tag)
			prog_count += 1
			text_lines.append(ijava_dict[tag] + "; ")

	if (prog_count > 0):
		text_lines.insert(0,
						  name + " worked on the iJava interactive online textbook and demonstrated understanding of the following concepts: ")
		line = text_lines[len(text_lines) - 1]
		line = line[:len(line)-2] + "."
		text_lines[len(text_lines) - 1] = "and " + line + "\n"

	prev_prog_count = prog_count
	prev_text_lines = text_lines
	text_lines = []

	goal_dict = OrderedDict([
		("{L1}" , "encapsulation with getters and setters"),
		("{L2}" , "interfaces and implementation"),
		("{L3}" , "inheritance of variables and methods"),
		("{L4}" , "polymorphism"),
		("{L5}" , "Java Collections API, namely HashMap and ArrayList"),
		("{L6}" , "unit testing, regression testing, and refactoring"),
		("{L7}" , "exceptions and the try / catch keywords"),
		("{L8}" , "enumerations"),
		("{L9}" , "incremental development using git and GitHub.")
	])

	for x in tags:
		tokens = x.split(":")
		tag = tokens[0].rstrip()
		results = re.search("\{L[0-9]*\}", tag)
		if (results != None):
			prog_count += 1
			text_lines.append(goal_dict[tag] + "; ")

	if (prog_count > prev_prog_count):
		text_lines.insert(0, name + " demonstrated understanding of the following learning goals: ")
		line = text_lines[len(text_lines) - 1]
		line = line[:len(line)-2] + "."
		text_lines[len(text_lines) - 1] = "and " + line + "\n"

	text_lines = prev_text_lines + text_lines

	if (prog_count >= 9 or override):
		cred_lines.append("4 - Java Programming II\n")
		text_lines.insert(0,
						  "In Programming as a Way of Life III, " + name + " became proficient in developing Java programs at a medium scale. ")
	else:
		# If there are not the threshold of 9 learning goals, reset everything to a blank eval
		text_lines = []

	return (text_lines, cred_lines)

generate_eval_text(sem_in_file, sem_out_file, sem_cred_file, [sem_callback, talk_callback])
generate_eval_text(prog_in_file, prog_out_file, prog_cred_file, [prog_callback])

if (prog_custom_file != None):
	custom_lines = prog_custom_file.readlines()
	prog_out_file.writelines(custom_lines)
	prog_custom_file.close()

close_file(sem_in_file, sem_out_file, sem_cred_file)
close_file(prog_in_file, prog_out_file, prog_cred_file)
