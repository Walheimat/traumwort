import random

def truncate(str):
	str = str.translate(None, ".,»«?:;!-_")
	str = " ".join(str.split())
	return str
	
def generate_set(txt):
	txt = truncate(txt)
	txt_arr = txt.split(" ")
	return set(txt_arr)
	
def generate_array(txt):
	txt = truncate(txt)
	txt_arr = txt.split(" ")
	return txt_arr
	
def generate_seed():
	sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']
	random.shuffle(sequence)
	sequence_as_string = str(sequence[0]) + str(sequence[1]) + str(sequence[2]) + str(sequence[3]) + str(sequence[4])
	return sequence_as_string