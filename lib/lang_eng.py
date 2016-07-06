def check_for_comma(word):
	if word.endswith('ing'):
		return True
	return False
	
def check_for_period(word):
	if word[0].isupper():
		if word not in names:
			return True
	return False
	
def find_names(txtarr):
	global names, commons
	
	names = []
	commons = []
	
	c = open('lib/commons/lang_eng.dt').read().split()
	for word in c:
		commons.append(word)
	
	candidates = {}
	
	for word in txtarr:
		if word[0].isupper():
			if word not in candidates:
				candidates[word] = 1
			else:
				candidates[word] += 1
	
	for word in candidates.keys():
		if candidates[word] > 2:
			if word not in commons:
				names.append(word)
				
	print(names)