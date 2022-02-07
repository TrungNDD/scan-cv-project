from ast import operator
from cProfile import label
from genericpath import isfile
from ntpath import join
from os import listdir
from  tkinter import *
from tkinter import messagebox
from turtle import title
from isort import file
from numpy import pad

from pip import main
from common import *
from convertPdf2Image import convertPdf2Image
import time

root = Tk()
root.title('LugHRM - Demo')
mainFrame = PanedWindow(root)
mainFrame.pack(fill=BOTH, expand=True,padx=20,pady=20)

bigLabelTxt = StringVar()
bigLabelTxt.set("LugHRM")

def applicantSelect(evt):
    filename = 'tmp/' + str(listSampleBox.get(listSampleBox.curselection()))

    with open(filename, 'r', encoding='utf8') as file:
        text = file.read()

    topLevel = Toplevel(root)
    topLevel.title(filename)
    
    textView = Text(topLevel,font=btnFont)
    textView.insert(END, text)
    textView.pack(side=LEFT)

    topLevel.resizable(False,False)
    topLevel.mainloop()


rightPanedWindow = PanedWindow(mainFrame, orient=VERTICAL)
mainFrame.add(rightPanedWindow)
# --ApplicantPoolFrame
applicantPoolFrame = Frame(root)

applicantPoolLabel = Label(applicantPoolFrame, text='Applicant Pool', font=headerFont)
applicantPoolLabel.pack(side=TOP)

listSampleBox = Listbox(applicantPoolFrame, font=btnFont)
listSampleBox.bind('<<ListboxSelect>>', applicantSelect)
listSampleBox.pack(side=BOTTOM,pady=10)

# ---ListSample to display
listSample = [filename for filename in listdir('tmp/') if '.txt' in filename]

for filename in listSample:
    listSampleBox.insert(END, filename)

print(listSample)

applicantPoolFrame.pack(side=TOP)
rightPanedWindow.add(applicantPoolFrame)
# --ApplicantPoolFrame

# ---addApplicantEvent
def addApplicantEvent():
    bigLabelTxt.set("Loading...")
    start = time.time()
    filename = addApplicant()
    print("Scanning executed time:---%s sec",time.time() - start)
    bigLabelTxt.set("LugHRM")

    if filename not in listSample: 
        listSample.append(filename)
        listSampleBox.insert(END, filename)
    root.update()

def simpleMethodEvent():
    start = time.time()
    points = simpleMethod()
    print("Simple method executed time:---%s sec",time.time() - start)
    points = sorted(points, key = lambda i: i['point'], reverse=True)
    topLevel = Toplevel(root)
    topLevel.title("Simple Method")

    for i in range(len(points)):
        for j in range(len(points[0])):
            cellFrame = Frame(topLevel,bg='white')
            cellFrame.grid(row=i+1, column=j)
            cellLabel = Entry(cellFrame, font=btnFont,width=(j%2+20),borderwidth=1,justify=LEFT)
            cellLabel.insert(END, points[i]['sample'] if (j==0) else points[i]['point'])
            cellLabel.config(state='disabled',bg='white')
            cellLabel.pack()

    topLevel.mainloop()

def tfidfMeasureEvent():
    start = time.time()
    points = tfidfMeasure()
    print("TF-IDF measure executed time:---%s sec",time.time() - start)
    points = sorted(points, key = lambda i: i['point'], reverse=True)
    topLevel = Toplevel(root)
    topLevel.title("Simple Method")

    for i in range(len(points)):
        for j in range(len(points[0])):
            cellFrame = Frame(topLevel,bg='white')
            cellFrame.grid(row=i+1, column=j)
            cellLabel = Entry(cellFrame, font=btnFont,width=(j%2+20),borderwidth=1,justify=LEFT)
            cellLabel.insert(END, points[i]['sample'] if (j==0) else points[i]['point'])
            cellLabel.config(state='disabled',bg='white')
            cellLabel.pack()

    topLevel.mainloop()

# ---MenuFrame
menuFrame = Frame(mainFrame)

bigLabel = Label(menuFrame, textvariable=bigLabelTxt, font=headerFont)
bigLabel.pack(side=TOP)

addApplicantBtn = Button(menuFrame, text="Scan Applicant's CV file",font=btnFont,width=btnWidth,command=addApplicantEvent)
addApplicantBtn.pack(side=TOP)

# addCriteriaBtn = Button(menuFrame, text="Add Criteria",font=btnFont,width=btnWidth)
# addCriteriaBtn.pack(side=TOP)

simpleMethodBtn = Button(menuFrame, text="Run Simple Method",font=btnFont,width=btnWidth,command=simpleMethodEvent)
simpleMethodBtn.pack(side=TOP)

tfidfMeasureBtn = Button(menuFrame, text="Run TF-IDF Method",font=btnFont,width=btnWidth,command=tfidfMeasureEvent)
tfidfMeasureBtn.pack(side=TOP)

menuFrame.pack(side=LEFT)
mainFrame.add(menuFrame)
# ---MenuFrame

# --CriteriaTableFrame
criteriaTableFrame = Frame(root)

criteriaTableLabel = Label(criteriaTableFrame, text='Criteria Table', font=headerFont)
criteriaTableLabel.pack(side=TOP)

tempFrame = Frame(criteriaTableFrame, width=20)
for i in range(len(criteriaTable)):
    for j in range(len(criteriaTable[0])):
        cellFrame = Frame(tempFrame,bg='white')

        cellFrame.grid(row=i, column=j)
        cellLabel = Entry(cellFrame, font=btnFont,width=(j%2)*15+5,borderwidth=1,justify=LEFT)
        cellLabel.insert(END,criteriaTable[i][j])
        cellLabel.config(state='disabled')
        cellLabel.pack()
        
tempFrame.pack()
criteriaTableFrame.pack(side=BOTTOM)
rightPanedWindow.add(criteriaTableFrame)
# --CriteriaTableFrame

root.resizable(False,False)
root.mainloop()


