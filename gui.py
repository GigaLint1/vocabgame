import tkinter as tk
from functions import new_word, new_sentence
import random
from tkinter import font

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
        self.bind_all('<Right>', self.nextdef)

        title = tk.Label(self, text='What is the correct definition of:', bg='#80c1ff', font=self.titlefont)
        title.grid(row=0, column= 1, sticky='nesw', ipadx=70, ipady=20, pady=20)

        self.word, self.correctdef, self.fakedef1, self.fakedef2 = new_word()

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

        backbtn = tk.Button(self, text="Back to home", justify='center', relief='groove', bg='white', font=self.helv36, command=lambda: controller.show_frame(HomePage))
        backbtn.grid(row=0, column=2, ipady=15, ipadx=15, padx=15, pady=15)

        outcome = tk.Label(self, font=self.qwordfont)
        outcome.grid(row=4, column=1)

        global defscore
        scores = tk.Label(self, text=f"Score: {str(defscore)}", font=self.helv36)
        scores.grid(row=5, column=2)
    
    def check(self, guess, outcome):
        if guess == self.correctdef:
            outcome.config(text = "correct", fg='green')
            self.correct = 1
            global defscore
            defscore += 1   
            nextbtn = tk.Button(self, text="Next (->)", justify='center', relief='groove', bg='white', font=self.helv36, command=lambda : self.nextdef())
            nextbtn.grid(row=1, column=2, ipady=20, ipadx=10, padx=20, pady=30)   

        else:
            if outcome['text'] == 'wrong':
                outcome.config(text = 'still wrong', fg='red')
            else:
                outcome.config(text = 'wrong', fg='red')
        
    def nextdef(self, event=None):
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
        self.bind_all('<Return>', self.nexteg)

        self.titlefont = font.Font(family='Arial', size=14, weight='bold')
        self.qwordfont = font.Font(family='Arial', size=14, weight='bold')
        self.helv36 = font.Font(family='Helvetica', size=10, weight='bold', underline=True)

        title = tk.Label(self,text='Fill in the blank with the correct word.', bg='#80c1ff', font=self.titlefont)
        title.grid(row=0, column= 1, sticky='nesw', ipadx=70, ipady=20, pady=40)

        self.sentence, self.correctword, self.fakeword1, self.fakeword2 = new_sentence()

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

        backbtn = tk.Button(self, text="Back to home", justify='center', relief='groove', bg='white', font=self.helv36, command=lambda: controller.show_frame(HomePage))
        backbtn.grid(row=0, column=2, ipady=15, ipadx=15, padx=15, pady=15)        

        outcome = tk.Label(self, font=self.qwordfont)
        outcome.grid(row=4, column=1)

        global egscore
        scores = tk.Label(self, text=f"Score: {str(egscore)}", font=self.helv36)
        scores.grid(row=5, column=2)   

    def check(self, guess, outcome):
        if guess == self.correctword:
            outcome.config(text = "correct", fg='green')
            global egscore
            egscore += 1
            nextbtn = tk.Button(self, text="Next (Enter)", justify='center', relief='groove', bg='white', font=self.helv36, command=lambda : self.nexteg())
            nextbtn.grid(row=1, column=2, ipady=20, ipadx=10, padx=20, pady=30)                
  
        else:
            if outcome['text'] == 'wrong':
                outcome.config(text = 'still wrong', fg='red')
            else:
                outcome.config(text = 'wrong', fg='red')
        
        
    def nexteg(self, event=None):
        global app
        app.after(100, app.frames[Examples].destroy())
        app.frames[Examples] = Examples(container, app)
        app.frames[Examples].grid(row=0, column = 0, sticky = "nsew")
        app.frames[Examples].tkraise()    

# Start main events loop
app = GuessingGame()
app.mainloop()
