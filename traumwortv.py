from Tkinter import *
import tkFileDialog
import threading

class ttThread (threading.Thread):
	
	def __init(self):
		threading.Thread.__init__(self)
	def run(self):
		import traumwort
		traumwort.load_file(path_to_text, v_diversity, v_noe, g_only, v_length, log_text)

def hello():
    print "hello!"
	
def open_file():
	global path_to_text
	
	path_to_text = file_path = tkFileDialog.askopenfilename(filetypes=[('text files', '.txt')])
	log_text.config(state=NORMAL)
	log_text.insert(END, "\nWir werden folgende Datei verwenden: ")
	log_text.insert(END, path_to_text)
	log_text.config(state=DISABLED)
	
	menubar.entryconfig("Los geht's!", state="normal")
	
def set_diversity():
	global v_diversity
	
	v_diversity = float(div_spin.get())
	
def set_noe():
	global v_noe
	
	v_noe = int(epoch_spin.get())
	
def set_length():
	global v_length
	
	v_length = int(leng_spin.get())
	
def go():
	test_thread = ttThread()
	test_thread.start()
	
def set_gen():
	global g_only

	if "nur generieren" in gen_spin.get():
		g_only = True
	elif "trainieren" in gen_spin.get():
		g_only = False
		
def info():
	log_text.config(state=NORMAL)
	log_text.insert(END, "\n\nGebrauchsanweisung kommt noch ...", "b")
	log_text.config(state=DISABLED)
	
global root, g_only, log_text, v_diversity, v_noe, v_length

v_diversity = 0.2
v_length = 20
v_noe = 1
g_only = True
root = Tk()
root.title("Traumwort")

menubar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Öffnen ...", command=open_file)
filemenu.add_separator()
filemenu.add_command(label="Beenden", command=root.quit)
menubar.add_cascade(label="Datei", menu=filemenu)

menubar.add_command(label="Los geht's!", command=hello)
menubar.entryconfig("Los geht's!", state="disabled", command=go)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Info ...", command=info)
menubar.add_cascade(label="Hilfe", menu=helpmenu)

# TEXT-LOG
lf_log = LabelFrame(root, text="Log")
lf_log.grid(row=0, column=0, padx=20, pady=20)
text_scr = Scrollbar(lf_log)
text_scr.pack(side=RIGHT, fill=Y)
log_text = Text(lf_log, width=80, height=20, yscrollcommand = text_scr.set, wrap=WORD)
log_text.pack()

# Farben
log_text.tag_config("b", foreground="blue")
log_text.tag_config("r", foreground="red")
log_text.tag_config("d", foreground="black")

log_text.insert(END, "VISUAL KETTCAT TRAUMWORT EDITION!", "r")
log_text.config(state=DISABLED)

lf_config = LabelFrame(root, text="Einstellungen")
lf_config.grid(row=0, column=1, padx=10, pady=10)

lf_gen = LabelFrame(lf_config, text="Modus")
lf_gen.pack(padx=10, pady=10)
gen_spin = Spinbox(lf_gen, values=("nur generieren", "trainieren"), command=set_gen, wrap=True)
gen_spin.pack()

lf_epoch = LabelFrame(lf_config, text="Epochen")
lf_epoch.pack(padx=10, pady=10)
epoch_spin = Spinbox(lf_epoch, values=(1, 5, 10, 20, 50), command=set_noe)
epoch_spin.pack()

lf_div = LabelFrame(lf_config, text="diversity")
lf_div.pack(padx=10, pady=10)
div_spin = Spinbox(lf_div, values=(0.2, 0.4, 0.6, 0.8, 1.0, 1.2), command=set_diversity)
div_spin.pack()

lf_leng = LabelFrame(lf_config, text="Textlänge")
lf_leng.pack(padx=10, pady=10)
leng_spin = Spinbox(lf_leng, values=(20, 50, 100, 200, 500, 1000), command=set_length)
leng_spin.pack()

# display the menu
root.config(menu=menubar)
root.mainloop()