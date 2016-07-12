def check_for_comma(word):
	global last_word
	
	if word in cond_comma:
		last_word = word
		return True
	elif "_".join([last_word, word]) in cond_comma:
		last_word = word
		return true
	last_word = word
	return False
	
def check_for_period(word):
	if word[0].isupper():
		if word in unlikely:
			return True
	return False
	
def find_cond(txtarr):
	global cond_comma, unlikely, last_word
	
	last_word = ""
	
	cond_comma = []
	unlikely = []
	
	c = open('twlib/commons/lang_deu_comma.dt').read().split()
	for word in c:
		cond_comma.append(word)
		
	u = open('twlib/commons/lang_deu_period.dt').read().split()
	for word in u:
		unlikely.append(word)