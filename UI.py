# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:06:06 2019

@author: Hengky Sanjaya
"""

from tkinter import filedialog
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
# import PIL as pl
# from PIL import Image, ImageTk
import PIL.Image
import PIL.ImageTk
import os
import tkinter.font as tkFont

from main_flowchart import draw_flowchart
#
# #open file https://pythonspot.com/tk-file-dialogs/
# root = Tk()
# root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
# print (root.filename)



# text editor

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title("Code to Flowchart")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

root=Tk()
root.title("Code to Flowchart")

scrollbar = Scrollbar(root)

#size of the window
root.geometry("730x630")



def open_file():
    filename = filedialog.askopenfilename(title="Select file",
                                          filetypes=(("C++ File", "*.cpp"), ("All Files", "*.*")))
    print(filename)
    txt.delete(1.0 , END)

    data = open(filename, mode='r').readlines()
    for i in data:
        print(i)
        if i[0] == '/' and i[1] == '/':
            txt.insert(INSERT, i, 'comment')
        else:
            txt.insert(INSERT, i)


    # txt.insert(INSERT, data)
    messagebox.showinfo("Information", "File imported successfully")


def convert():
    code = txt.get("1.0","end-1c")
    text_var.set('')
    error_message = draw_flowchart(code)


    print("error (ui.py)", error_message)

    if(error_message != None):
        text_var.set(str(error_message))



    # w = Label(root, text=str(error_message), fg='red')
    # w.pack()

    # x = 'flowchart.gv.png'
    #
    # img = PIL.Image.open(x)
    # # img = img.resize((400, 400), PIL.Image.ANTIALIAS)
    # img = PIL.ImageTk.PhotoImage(img)
    # # panel = Label(root, image=img)
    # # panel.image = img
    # # panel.place(x=500, y = 10)
    #
    # canv = Canvas(root, relief=SUNKEN)
    # canv.config(width=400, height=200)
    # canv.config(highlightthickness=0)
    # sbarV = Scrollbar(root, orient=VERTICAL)
    # sbarH = Scrollbar(root, orient=HORIZONTAL)
    # sbarV.config(command=canv.yview)
    # sbarH.config(command=canv.xview)
    # canv.config(yscrollcommand=sbarV.set)
    # canv.config(xscrollcommand=sbarH.set)
    # sbarV.pack(side=RIGHT, fill=Y)
    # sbarH.pack(side=BOTTOM, fill=X)
    # canv.pack(side=LEFT, expand=YES, fill=BOTH)
    #
    # width, height = 50,50
    # canv.config(scrollregion=(0, 0, width, height))
    # canv.create_image(0, 0, anchor="nw", image=img)



    # panel.pack()

    # img = ImageTk.PhotoImage(Image.open("flowchart.gv.png"))
    # panel = Label(root, image=img)
    # panel.pack(side="bottom", fill="both", expand="yes")

bigFont = tkFont.Font(family='Monaco', size=11, weight='bold')
txt = scrolledtext.ScrolledText(root, height=23, width=77,font = bigFont, bg='#222222', fg='#EEEEEE')

txt.grid(column=0, row=0)
txt.place(x=10, y= 190)
txt.config(insertbackground='#EEEEEE')

# txt.insert(END, "Ehila", 'name')  # <-- tagging `name`
# txt.insert(END, "Now", 'time')  # <-- tagging `time`
# txt.tag_config('loop', foreground='green')  # <-- Change colors of texts tagged `name`
# txt.tag_config('curly', foreground='red')
# txt.tag_config('variable', foreground='blue')
txt.tag_config('comment', foreground='green')


# textBox = Text(self, height=50, width=50)
# # textBox.pack()
# textBox.place(x=0, y=150)

# creating a menu instance
menu = Menu(root)
root.config(menu=menu)

file = Menu(menu)

# adds a command to the menu option, calling it exit, and the
# command it runs on event is client_exit
file.add_command(label="Import C++ File", command=lambda: open_file())

# added "file" to our menu
menu.add_cascade(label="File", menu=file)

# creating a button instance
convertBtn = Button(root, text="Convert", command=lambda: convert(),bg='#00579a',fg='#ecf0f1', height=1, width=98)

# placing the button on my window
convertBtn.place(x=10, y=590)


img = PIL.Image.open('logo/logo_1.png')
img = img.resize((350, 150), PIL.Image.ANTIALIAS)
img = PIL.ImageTk.PhotoImage(img)
panel = Label(root, image=img)
panel.image = img
panel.place(x=10, y = 10)


img2 = PIL.Image.open('logo/logo_2.png')
img2 = img2.resize((350, 150), PIL.Image.ANTIALIAS)
img2 = PIL.ImageTk.PhotoImage(img2)
panel2 = Label(root, image=img2)
panel2.image = img2
panel2.place(x=350, y = 10)


text_var = StringVar(root)
lbl = Label(root, textvariable=text_var, fg='red')
lbl.place(x=10, y=167)
# lbl.pack()


# def retrieve_input():
#    inputValue=textBox.get("1.0","end-1c")
#    print(inputValue)

# textBox=Text(root, height=30, width=150)
# textBox.pack()
# buttonCommit=Button(root, height=1, width=10, text="Commit",
#                    command=lambda: retrieve_input())
# command=lambda: retrieve_input() >>> just means do this when i press the button
# buttonCommit.pack()

root.mainloop()
