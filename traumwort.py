from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file
from keras.models import model_from_json
import keras.callbacks
import numpy as np
import random
import getopt
import sys
sys.path.insert(0, './lib')
import locale
import os
import str_manipulation as manip

# Verluste	
class LossHistory(keras.callbacks.Callback):
	def on_train_begin(self, logs={}):
		self.losses = []

	def on_batch_end(self, batch, logs={}):
		self.losses.append(logs.get('loss'))

# Pfaderstellung
def get_path_and_file(pth, nm, md):
	directory = pth + '/'
	if not os.path.exists(directory):
		os.makedirs(directory)
	fl = open(directory + nm + '.' + pth, md)
	return fl

# Hilfe
def usage():
	try:
		help = open('stuff/help.dt')
		print(help.read())
	except IOError as err:
		print(err)

# Einlesen und Verarbeiten des Texts		
def read_text(path):
	global words, text_as_words, word_indices, indices_word

	if is_lower:
		text = open(path).read().lower()
	else:
		text = open(path).read()

	words = manip.generate_set(text)
	text_as_words = manip.generate_array(text)

	word_indices = dict((c, i) for i, c in enumerate(words))
	indices_word = dict((i, c) for i, c in enumerate(words))
	
	print('Textlänge:', len(text))
	print('Anzahl der Wörter:', len(words))
	
# Vektorisierung der Wörter
def vectorize():
	global max_number_of_words, word_sequences, next_words, X, y
		
	max_number_of_words = 10
	step = 3
	word_sequences = []
	next_words = []
	
	for i in range (0, len(text_as_words) - max_number_of_words, step):
		seq = []
		for t in range(0, max_number_of_words):
			seq.append(text_as_words[i + t])
		word_sequences.append(seq)
		next_words.append(text_as_words[i + max_number_of_words])
	print('nb-Sequenzen:', len(word_sequences))

	print('es wird vektorisiert...')
	X = np.zeros((len(word_sequences), max_number_of_words, len(words)), dtype=np.bool)
	y = np.zeros((len(word_sequences), len(words)), dtype=np.bool)
	for i, sequence in enumerate(word_sequences):
		for t, word in enumerate(sequence):
			X[i, t, word_indices[word]] = 1
		y[i, word_indices[next_words[i]]] = 1

# Modellerstellung		
def build_model():
	global model

	print('Modell wird erstellt...', '\n')
	if fresh:
		model = Sequential()
		model.add(LSTM(512, return_sequences=True, input_shape=(max_number_of_words, len(words))))
		model.add(Dropout(0.2))
		model.add(LSTM(512, return_sequences=False))
		model.add(Dropout(0.2))
		model.add(Dense(len(words)))
		model.add(Activation('softmax'))
		model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
		
		get_path_and_file('json', input_trunc, 'w').write(model.to_json())
	else:
		model = model_from_json(get_path_and_file('json', input_trunc, 'r').read())
		model.load_weights('weights/' + input_trunc + '.hdf5')
		model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
	
# Training
def train_network():
	global history
	
	history = LossHistory()
	model.fit(
		X,
		y,
		batch_size=128,
		nb_epoch=no_of_epochs,
		verbose=1,
		callbacks=[history]
	)
	
# könnte man bei Bedarf auch ändern
def sample(a, temperature=1.0):
	# helper function to sample an index from a probability array
	a = np.log(a) / temperature
	a = np.exp(a) / np.sum(np.exp(a))
	return np.argmax(np.random.multinomial(1, a, 1))
	
	
def generate_text():
	print('Generierung läuft...')
	
	start_index = random.randint(0, len(text_as_words) - max_number_of_words - 1)
	
	sequence = []
	for i in range (start_index, start_index + max_number_of_words):
		sequence.append(text_as_words[i])
	generated = ""
	generated += " ".join(sequence)
	
	# hier wird live generiert
	for i in range(output_length):
		x = np.zeros((1, max_number_of_words, len(words)))
		for t, word in enumerate(sequence):
			x[0, t, word_indices[word]] = 1.

		preds = model.predict(x, verbose=0)[0]
		next_index = sample(preds, diversity)
		next_word = indices_word[next_index]
		
		if grammar.check_for_comma(next_word):
			generated += ', ' + next_word
		elif grammar.check_for_period(next_word):
			generated += '. ' + next_word
		else:
			generated += ' ' + next_word
		
		del sequence[0]
		sequence.append(next_word)

		if not muted:
			# den Stream kannst du sicher auch mit dem Drucker verbinden; sonst halt die Datei einlesen
			sys.stdout.write(next_word)
			sys.stdout.write(' ')
			sys.stdout.flush()
	
	# hier wird in die Datei geschrieben
	save_text(generated)
	
	print("\nDer versuchsweise rekonstruierte Text:\n")
	print(generated)
	
def save_text(txt):
	directory = 'output/' + input_trunc + '/'
	if not os.path.exists(directory):
		os.makedirs(directory)

	random_seed = manip.generate_seed()
	output_name = random_seed + '.txt'
	output_file = open(directory + output_name, 'w')
	output_file.write(txt)
	print()
	print("Die Ausgabe findest du hier: " + directory + output_name)

def main():
	global input_trunc, output_length, muted, diversity, no_of_epochs, is_lower, fresh, language, grammar

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:nrgl:d:e:c")
	except getopt.GetoptError as err:
		print(str(err))
		usage()
		sys.exit(2)
	language = "English"
	input = None
	fresh = False
	is_lower = False
	no_of_epochs = 10
	generate_only = False
	output_length = 20
	diversity = 0.2
	muted = False
	for o, a in opts:
		if o == "-h":
			usage()
			sys.exit(2)
		elif o in ("-i"):
			input = a
		elif o in ("-n"):
			fresh = True
			generate_only = False
		elif o in ("-r"):
			generate_only = False
		elif o in ("-g"):
			generate_only = True
		elif o in ("-l"):
			output_length = int(a)
		elif o in ("-d"):
			diversity = float(a)
			if diversity > 2.0:
				diversity = 2.0
		elif o in ("-e"):
			no_of_epochs = int(a)
		elif o in ("-c"):
			is_lower = True
		elif o in ("-m"):
			muted = True
		else:
			assert False, "unhandled option"
	if input is None:
		usage()
		sys.exit(2)
	
	input_trunc = input[:(len(input) - 4)]
	
	if "English" in language:
		import lang_eng as grammar
	
	# ich hoffe, das funktioniert auch auf Linux/OS X; dieses ganze Decoding und Encoding ist eigentlich nur für die richtige Darstellung im Terminal
	# intern ist sowieso alles utf-8-codiert
	print('=' * 12)
	print("TRAUMTEXT.PY")
	print('=' * 12, "\n")
	print("Wir verwenden folgenden Text:", input)
	if generate_only:
		print("Es wird, ausgehend von der gespeicherten Gewichtsmatrix ein {0}-Zeichen langer Text mit diversity-Grad {1} generiert...".format(output_length, diversity))
	else:
		print("Das Netzwerk wird {0} Epoche(n) lang trainiert!".format(no_of_epochs))
	
	read_text(input)
	grammar.find_names(text_as_words)
	vectorize()
	build_model()

	if not generate_only:
		train_network()
		model.save_weights('weights/' + input_trunc + '.hdf5', overwrite=True)
		losses_sum = 0.0
		for i in history.losses:
			losses_sum += float(i)
		print('Durchschnitt:', round(losses_sum / len(history.losses), 10))
		
	generate_text()
	
	print("\n", '=' * 24)
	print("TRAUMTEXT.PY SAGT DANKE!")
	print('=' * 24)

if __name__ == "__main__":
	main()
