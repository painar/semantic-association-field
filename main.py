from tkinter import *
from tkinter import filedialog
import logging
from vec2graph import visualize
import gensim
import nltk
from nltk.tokenize import word_tokenize
import string
import ctypes
OUTPUT_DIR = '/Users/an/desktop/graph'
logging.basicConfig(level=logging.INFO)
from cefpython3 import cefpython as cef
import os 
from tkinter import messagebox

class TokenizedSentences:

    def __init__(self, filename: str):
        self.filename = filename

    def __iter__(self):
        with open(self.filename, encoding='utf-8') as f:
            corpus = f.read()
        
        
        raw_sentences = nltk.tokenize.sent_tokenize(corpus)
        
        for sentence in raw_sentences:
            if len(sentence) > 0:
                yield gensim.utils.simple_preprocess(sentence, min_len=2)


def loadInfo():
	text = "Ассоциативно-семантическое поле определяется как семантическое поле, где границы данного поля значительно расширяются за счет включения в его состав лексики, соотносимой с ядром поля по принципу ассоциации. \nВершины, не соединенные друг с другом ребром не превышают заданный порог близости по косинусному сходству."
	messagebox.showinfo("Информация",text)



def loadText(): 
	global filename
	root.filename = filedialog.askopenfilename(initialdir='/',title ='Выберите файл',filetypes=[("Text files","*.txt")])
	if root.filename:
		selecttext = Label(frame, text = 'Выбранный файл - '+ os.path.basename(root.filename)).pack()
		trainbutton.pack(padx=5, pady=5)
	else:
		pass
	
def trainmodel():
	global model
	sentences = TokenizedSentences(root.filename)
	model = gensim.models.word2vec.Word2Vec(sentences=sentences,
             sg=1,  # 0 for CBOW and 1 for Skip-gram
             sample = 1e-3,
             hs = 1,
             #workers = 2,
             size=300,  
             window=5,  
             negative=20,  
             min_count=5,  
             iter=10 #20
             )        
	completelabel = Label(frame, text = 'Модель создана').pack()
	text1.pack()
	e.pack()
	text2.pack()
	nWords.pack()
	text3.pack()
	scale.pack(anchor=CENTER)
	buttonWord.pack(padx=5, pady=5)
	listframe.pack()

def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True 

def onScreen():
	words = [word_asf]
	topn =  int(nword_asf) - 1
	threshold = var.get()
	visualize(OUTPUT_DIR, model.wv, word_asf, depth=0, topn=topn, threshold=float(threshold), edge=1, sep=True)
	topn = int(topn)
	for word in words:
		if word in model:
			Label(listframe, text = word).pack()
			for i in model.wv.most_similar(positive=[word], topn=int(topn)):
            	# слово и коэффициент косинусной близости
				Label(listframe, text = (i[0],'-', i[1])).pack()
			visBtn = Button(listframe, text = 'Визуализировать',command = wGraph).pack()
		else:
			Label(listframe, text = 'Cлово \"%s\" отсутствует в модели.'%(word)).pack()	

def wGraph():
	cef.Initialize()
	cef.CreateBrowserSync(url='file:///C:/Users/AN/Desktop/graph/%s.html'%(word_asf))
	cef.MessageLoop()

def submitWord():
	global word_asf
	global nword_asf
	for widget in listframe.winfo_children():
		widget.destroy()
	word_asf = e.get()
	nword_asf = nWords.get()
	wordlabel = Label(listframe, text = onScreen()).pack()
	
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

root = Tk()
root.title("Визуализация АСП")

#create a widget
canvas = Canvas(root)
frame = Frame(canvas)
vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")
canvas.pack(fill="both", expand=True)
canvas.create_window((3,3), window=frame, anchor="nw")
frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

listframe = Frame(frame)
firstlabel = Label(frame, text = ' ',width =53)
e = Entry(frame)
submitbutton = Button(frame, text = 'Выбрать текст',command = loadText)
infobutton = Button(frame, text = 'Информация', command = loadInfo)
trainbutton = Button(frame,text = "Создать модель",command = trainmodel)
buttonWord = Button(frame, text='Создать поле',command = submitWord)
nWords = Entry(frame, validate="key")
nWords['validatecommand'] = (nWords.register(testVal),'%P','%d')
var = DoubleVar()
scale = Scale(frame, variable = var,length= 130, orient=HORIZONTAL, from_ =0.1, to = 0.9, resolution= 0.05 )
text1 = Label(frame,text="Введите слово:")
text2 = Label(frame,text="Введите размер поля:")
text3 = Label(frame,text="Введите минимальное значение \nкосинусной близости:")
#output
firstlabel.pack()
submitbutton.place( x = 95 ,y= 20)
infobutton.place(x=210,y=20)

separator = Frame(frame,height=2, bd=1, relief=SUNKEN)
separator.pack(fill=X, padx=5, pady=35)

root.mainloop()