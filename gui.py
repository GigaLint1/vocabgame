import tkinter as tk
import csv
import random
from tkinter import font
import re

defscore = 0   
egscore = 0

# Initiator
class GuessingGame(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        global container
        container = tk.Frame(self)
        container.pack()

        self.frames = {}

        for f in (HomePage, Definitions, Examples):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(HomePage)

    def show_frame(self, containr):

        frame = self.frames[containr]
        frame.tkraise()

# Home Page
class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.btnfont = font.Font(family='Helvetica', size=20, weight='bold')
        self.titlefont = font.Font(family='Helvetica', size=35, weight='bold')
        title = tk.Label(self, text='Vocab guessing game.', font=self.titlefont)
        title.grid(row=0, column=1, pady=100)

        def_btn = tk.Button(self, text='Definitions', fg='blue', font=self.btnfont, command=lambda: controller.show_frame(Definitions))
        def_btn.grid(row=1, column=0, padx=50, pady=100, ipadx=50)

        eg_btn = tk.Button(self, text='Examples', fg='green', font=self.btnfont, command=lambda: controller.show_frame(Examples))
        eg_btn.grid(row=1, column=2, padx=50, pady=100, ipadx=50)

# Definitions 
class Definitions(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.titlefont = font.Font(family='Arial', size=20, weight='bold')
        self.qwordfont = font.Font(family='Arial', size=20, weight='bold', underline=True)
        self.helv36 = font.Font(family='Helvetica', size=10, weight='bold')

        title = tk.Label(self, text='What is the correct definition of:', bg='#80c1ff', font=self.titlefont)
        title.grid(row=0, column= 1, sticky='nesw', ipadx=70, ipady=20, pady=20)

        self.new_word()

        qword = tk.Label(self, text=self.word.title(), bg='#80c1ff', font=self.qwordfont)
        qword.grid(row=1, column=1, ipadx=150, ipady=30, pady=50)
        
        lst = [0, 1, 2]
        random.shuffle(lst)

        b1 = tk.Button(self, text=self.fakedef1, justify='center', relief='groove', wraplength=300, bg='white', font=self.helv36, command=lambda a=self.fakedef1: self.check(a, outcome))
        b1.grid(row=2, rowspan=2, column=lst[0], ipady=20, ipadx=10, padx=20, pady=30)

        b2 = tk.Button(self, text=self.fakedef2, justify='center', relief='groove', wraplength=300, bg='white', font=self.helv36, command=lambda a=self.fakedef2: self.check(a, outcome))
        b2.grid(row=2, rowspan=2, column=lst[1], ipady=20, ipadx=10, padx=20, pady=30)

        b3 = tk.Button(self, text=self.correctdef, justify='center', relief='groove', wraplength=300, bg='white', font=self.helv36, command=lambda a=self.correctdef: self.check(a, outcome))
        b3.grid(row=2, rowspan=2, column=lst[2], ipady=20, ipadx=10, padx=20, pady=30)

        outcome = tk.Label(self, font=self.helv36)
        outcome.grid(row=4, column=1)

        global defscore
        scores = tk.Label(self, text=f"Score: {str(defscore)}", font=self.helv36)
        scores.grid(row=5, column=2)

    def new_word(self):
        self._words = []
        with open('dictionary.csv', 'r') as dictionary:
            reader = csv.DictReader(dictionary, fieldnames=['word', 'type', 'definitions', 'examples'])
            for row in reader:
                self._words.append(row)
        self.word = random.choice(self._words[1:])['word']
        for i in self._words[1:]:
            if i['word'] == self.word:
                self.correctdef = re.sub(r"[(\[\')(\'\])]", ' ', i['definitions'])
                self._words.pop(self._words.index(i))
        self._fakes = random.sample(self._words, 2)
        self.fakedef1 = re.sub(r"[(\[\')(\'\])]", ' ', self._fakes[0]['definitions'])
        self.fakedef2 = re.sub(r"[(\[\')(\'\])]", ' ', self._fakes[1]['definitions'])
    
    def check(self, guess, outcome):
        if guess == self.correctdef:
            outcome.config(text = "correct", fg='green')
            global defscore
            defscore += 1   
            self.nextslide()     

        else:
            if outcome['text'] == 'wrong':
                outcome.config(text = 'still wrong', fg='red')
            else:
                outcome.config(text = 'wrong', fg='red')
        
        
    def nextslide(self):
        global app
        app.after(100, app.frames[Definitions].destroy())
        app.frames[Definitions] = Definitions(container, app)
        app.frames[Definitions].grid(row=0, column = 0, sticky = "nsew")
        app.frames[Definitions].tkraise()

# Examples
class Examples(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller 

        self.titlefont = font.Font(family='Arial', size=14, weight='bold')
        self.qwordfont = font.Font(family='Arial', size=14, weight='bold')
        self.helv36 = font.Font(family='Helvetica', size=10, weight='bold', underline=True)

        title = tk.Label(self,text='Fill in the blank with the correct word.', bg='#80c1ff', font=self.titlefont)
        title.grid(row=0, column= 1, sticky='nesw', ipadx=70, ipady=20, pady=40)

        self.new_sentence()

        qsentence = tk.Label(self, text=self.sentence, bg='#80c1ff', font=self.qwordfont, wraplength=350)
        qsentence.grid(row=1, column=1, ipadx=100, ipady=30, pady=50)
        
        lst = [0, 1, 2]
        random.shuffle(lst)

        b1 = tk.Button(self, text=self.fakeword1, justify='center', relief='groove', wraplength=300, bg='white', font=self.helv36, command=lambda a=self.fakeword1: self.check(a, outcome))
        b1.grid(row=2, rowspan=2, column=lst[0], ipady=20, ipadx=10, padx=20, pady=30)

        b2 = tk.Button(self, text=self.fakeword2, justify='center', relief='groove', wraplength=300, bg='white', font=self.helv36, command=lambda a=self.fakeword2: self.check(a, outcome))
        b2.grid(row=2, rowspan=2, column=lst[1], ipady=20, ipadx=10, padx=20, pady=30)

        b3 = tk.Button(self, text=self.correctword, justify='center', relief='groove', wraplength=300, bg='white', font=self.helv36, command=lambda a=self.correctword: self.check(a, outcome))
        b3.grid(row=2, rowspan=2, column=lst[2], ipady=20, ipadx=10, padx=20, pady=30)

        outcome = tk.Label(self, font=self.helv36)
        outcome.grid(row=4, column=1)

        global egscore
        scores = tk.Label(self, text=f"Score: {str(egscore)}", font=self.helv36)
        scores.grid(row=5, column=2)

    def new_sentence(self):
        self._sentences = []
        self._haveexamples = []
        with open('dictionary.csv', 'r') as dictionary:
            reader = csv.DictReader(dictionary, fieldnames=['word', 'type', 'definitions', 'examples'])
            for row in reader:
                self._sentences.append(dict(row))

        for i in self._sentences:
            if i['examples'] != "['No examples']":     
                i['examples'] = re.sub(r"[(\[\[)(\]\])]", '', i['examples']).split("', '")
                self._haveexamples.append(i)

        self._sentence = random.choice(self._haveexamples[1:])['examples']       
        if len(self._sentence) > 1:
            self.sentence = " / \n".join(self._sentence)
        else:
            self.sentence = self._sentence[0]

        for i in self._haveexamples[1:]:
            if i['examples'] == self._sentence:
                self.correctword = i['word']
                self._sentences.pop(self._sentences.index(i))
                self.sentence = self.sentence.replace(self.correctword, '______').rstrip("\"'").lstrip("\"'")               

        self._fakes = random.sample(self._sentences[1:], 2)
        self.fakeword1 = self._fakes[0]['word']
        self.fakeword2 = self._fakes[1]['word']      

    def check(self, guess, outcome):
        if guess == self.correctword:
            outcome.config(text = "correct", fg='green')
            global egscore
            egscore += 1   
            self.nextslide()     

        else:
            if outcome['text'] == 'wrong':
                outcome.config(text = 'still wrong', fg='red')
            else:
                outcome.config(text = 'wrong', fg='red')
        
        
    def nextslide(self):
        global app
        app.after(100, app.frames[Examples].destroy())
        app.frames[Examples] = Examples(container, app)
        app.frames[Examples].grid(row=0, column = 0, sticky = "nsew")
        app.frames[Examples].tkraise()    

# Start main events loop
app = GuessingGame()
app.mainloop()
