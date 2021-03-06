#streamcontrol v1.0 created by Casey Crocamo

#imports
import tkinter
from tkinter import *
import sys
import os
import csv
import mysql.connector
import atexit

#***************************AUTOCOMPLETE CODE***********************************************

tkinter_umlauts=['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']

class AutocompleteEntry(tkinter.Entry):
        """
        Subclass of tkinter.Entry that features autocompletion.
        
        To enable autocompletion use set_completion_list(list) to define 
        a list of possible strings to hit.
        To cycle through hits use down and up arrow keys.
        """
        def set_completion_list(self, completion_list):
                self._completion_list = completion_list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)               

        def autocomplete(self, delta=0):
                """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.startswith(self.get().lower()):
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,tkinter.END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,tkinter.END)
                        
        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(tkinter.INSERT), tkinter.END) 
                        self.position = self.index(tkinter.END)
                if event.keysym == "Left":
                        if self.position < self.index(tkinter.END): # delete the selection
                                self.delete(self.position, tkinter.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, tkinter.END)
                if event.keysym == "Right":
                        self.position = self.index(tkinter.END) # go to end (no selection)
                if event.keysym == "Down":
                        self.autocomplete(1) # cycle to next hit
                if event.keysym == "Up":
                        self.autocomplete(-1) # cycle to previous hit
                # perform normal autocomplete if event is a single key or an umlaut
                if len(event.keysym) == 1 or event.keysym in tkinter_umlauts:
                        self.autocomplete()


#*********************************************END AUTOCOMPLETE CODE***************************************

#global variables
names = ['Game', "Left Player", 'Right Player', 'Left Score', 'Right Score', 'Round', 'Commentary1', 'Commentary2']
rounds = ['Winners Round 1', 'Winners Round 2', 'Winners Round 3', 'Winners Round 4', 'Winners Round 5', 'Winners Round 5', 'Winners Quarters BO5', 'Winners Semis BO5', 'Winners Finals BO5', 'Losers Round 1', 'Losers Round 2', 'Losers Round 3', 'Losers Round 4', 'Losers Round 5', 'Losers Round 5', 'Losers Quarters BO5', 'Losers Semis BO5', 'Losers Finals BO5', 'Grand Finals BO5']
socialMediaData = {}
nameData = []
fieldsDict = {}
index = []
DB_NAME = 'streamcontrol'

#methods

def create_scoreboard(cursor, fields):
    cursor.execute('DROP TABLE IF EXISTS scoreboard')
    sql = 'CREATE TABLE scoreboard ('
    for name in fields:
            sql += name + ', '
            
    sql = sql[:-2]
    sql += ')'
    cursor.execute(sql)

def createLabels(window, names):
    for r in range(len(names)):
        for c in range(1):
            Label(window, text = names[r]).grid(row = r, column = c, sticky = 'E')

def generateFieldsDict():
        try:
                temp = gamebox.curselection()
                fieldsDict['game'] = '"' + gamebox.get(temp[0]) + '"'
                fieldsDict['playerLeft'] = '"' + playerLeftEntry.get() + '"'
                fieldsDict['playerRight'] = '"' + playerRightEntry.get() + '"'
                if(scoreLeftEntry.get() != ""):
                        fieldsDict['scoreLeft'] = scoreLeftEntry.get()
                else:
                        fieldsDict['scoreLeft'] = 0
                if(scoreRightEntry.get() != ""):
                        fieldsDict['scoreRight'] = scoreRightEntry.get()
                else:
                        fieldsDict['scoreRight'] = 0
                fieldsDict['round'] = '"' + roundEntry.get() + '"'
                fieldsDict['commentary1'] = '"' + commentary1Entry.get() + '"'
                fieldsDict['commentary2'] = '"' + commentary2Entry.get() + '"'
                fieldsDict['socPlayerLeft'] = '"' + socPlayerLeftEntry.get() + '"'
                fieldsDict['socPlayerRight'] = '"' + socPlayerRightEntry.get() + '"'
                fieldsDict['socCommentary1'] = '"' + socCommentary1Entry.get() + '"'
                fieldsDict['socCommentary2'] = '"' + socCommentary2Entry.get() + '"'
                fieldsDict['iconPlayerLeft'] = '"twitch"'
                fieldsDict['iconPlayerRight'] = '"twitch"'
                fieldsDict['iconCommentary1'] = '"twitch"'
                fieldsDict['iconCommentary2'] = '"twitch"'
                temp = colorBoxLeft.curselection()
                fieldsDict['colorPlayerLeft'] = '"' + colorBoxLeft.get(temp[0]) + '"'
                temp = colorBoxRight.curselection()
                fieldsDict['colorPlayerRight'] = '"' + colorBoxRight.get(temp[0]) + '"'
        except(NameError):
                print('One or more fields missing values')
        return fieldsDict
        
def modifyIndex(index, name, value):
    index[name] = value

def update():
    generateFieldsDict()
    #print(fieldsDict)
    for i in fieldsDict:
        updateSQL(cursor, i, fieldsDict[i])

def updateSQL(cursor, column, value):
    sql = 'INSERT INTO scoreboard(' + column + ') VALUES(' + str(value) + ')'
    print(sql)
    #if(value != ""):
    cursor.execute(sql)

def printIndex():
    print(index)
    
def addSM():
    loadCSV()
    try:
        socPlayerLeftEntry.delete(0,"end")
        socPlayerLeftEntry.insert(0, socialMediaData[playerLeftEntry.get()])
        index['socPlayerLeft'] = socialMediaData[playerLeftEntry.get()]
        
        socPlayerRightEntry.delete(0,"end")
        socPlayerRightEntry.insert(0, socialMediaData[playerRightEntry.get()])
        index['socPlayerRight'] = socialMediaData[playerRightEntry.get()]

        
        socCommentary1Entry.delete(0,"end")
        socCommentary1Entry.insert(0, socialMediaData[commentary1Entry.get()])
        index['socCommentary1'] = socialMediaData[commentary1Entry.get()]

        
        socCommentary2Entry.delete(0,"end")
        socCommentary2Entry.insert(0, socialMediaData[commentary2Entry.get()])
        index['socCommentary2'] = socialMediaData[commentary2Entry.get()]
        
    except(KeyError):
        print('no social media tag for one or more fields')

def switchLeftRight():
    temp = index['playerLeft']
    index['playerLeft'] = index['playerRight']
    index['playerRight'] = temp

    temp = index['scoreLeft']
    index['scoreLeft'] = index['scoreRight']
    index['scoreRight'] = temp

    temp = index['socPlayerLeft']
    index['socPlayerLeft'] = index['socPlayerRight']
    index['socPlayerRight'] = temp

    loadTextFields()

def clearTextFields():
    gameEntry.delete(0, 'end')
    playerLeftEntry.delete(0, 'end')
    playerRightEntry.delete(0, 'end')
    scoreLeftEntry.delete(0, 'end')
    scoreRightEntry.delete(0, 'end')
    roundEntry.delete(0, 'end')
    commentary1Entry.delete(0, 'end')
    commentary2Entry.delete(0, 'end')
    socPlayerLeftEntry.delete(0, 'end')
    socPlayerRightEntry.delete(0, 'end')
    socCommentary1Entry.delete(0, 'end')
    socCommentary2Entry.delete(0, 'end')
    
def updateIcons(index):
    try:
        if '@' in index['socPlayerLeft']:
            index['iconPlayerLeft'] = 'twitter'
        else:
            index['iconPlayerLeft'] = 'twitch'

        if '@' in index['socPlayerRight']:
            index['iconPlayerRight'] = 'twitter'
        else:
            index['iconPlayerRight'] = 'twitch'

        if '@' in index['socCommentary1']:
            index['iconCommentary1'] = 'twitter'
        else:
            index['iconCommentary1'] = 'twitch'

        if '@' in index['socCommentary2']:
            index['iconCommentary2'] = 'twitter'
        else:
            index['iconCommentary2'] = 'twitch'
    except(KeyError):
        print('one or more of the fields are missing values')
    return index 

def clearField(event):
    event.widget.delete(0, 'end')
    
def closing(cursor):
        print('Dropping tables and exiting database...')
        cursor.execute("DROP TABLE scoreboard")
        cursor.close()
        cnx.close()
        
#connect to mysql
cnx = mysql.connector.connect(user='root', password = '6549pardall', database = 'streamcontrol')
cursor = cnx.cursor()
name = 'scoreboard'
print("Creating table: " + name)
scoreboardfields = ['game CHAR(10)', 'playerLeft CHAR(50)', 'playerRight CHAR(50)', 'socPlayerLeft CHAR(25)', 'socPlayerRight CHAR(25)', 'commentary1 CHAR(50)', 'commentary2 CHAR(50)', 'socCommentary1 CHAR(25)', 'socCommentary2 CHAR(25)', 'colorPlayerLeft CHAR(5)', 'colorPlayerRight CHAR(5)', 'iconPlayerLeft CHAR(7)', 'iconPlayerRight CHAR(7)', 'iconCommentary1 CHAR(7)', 'iconCommentary2 CHAR(7)', 'scoreLeft INT(1)', 'scoreRight INT(1)', 'round CHAR(50)'] 
create_scoreboard(cursor, scoreboardfields)

#drop scoreboard and close server at exit
atexit.register(closing, cursor)

#draw tkinter window
top = Tk()
top.title('StreamControl v2.0')
top.iconbitmap(default = 'sif.ico')
#widgets
#labels
createLabels(top, names)
colorPlayerLeftLabel = Label(top, text = 'Color').grid(row = 1, column = 4, sticky = 'E')
colorPlayerRightLabel = Label(top, text = 'Color').grid(row = 2, column = 4, sticky = 'E')
socPlayerLeftLabel = Label(top, text = 'Social Media').grid(row = 1, column = 2, sticky = 'E')
socPlayerRightLabel = Label(top, text = 'Social Media').grid(row = 2, column = 2, sticky = 'E')
socCommentary1Label = Label(top, text = 'Social Media').grid(row = 6, column = 2, sticky = 'E')
socCommentary2Label = Label(top, text = 'Social Media').grid(row = 7, column = 2, sticky = 'E')

#entry fields
#gameEntry = AutocompleteEntry(top)
#gameEntry.grid(row = 0, column = 1)
#gameEntry.bind("<Button-1>", clearField)

playerLeftEntry = AutocompleteEntry(top)
#playerLeftEntry.set_completion_list(nameData)
playerLeftEntry.grid(row = 1, column = 1)
#playerLeftEntry.bind("<Button-1>", clearField)

playerRightEntry = AutocompleteEntry(top)
#playerRightEntry.set_completion_list(nameData)
playerRightEntry.grid(row = 2, column = 1)
#playerRightEntry.bind("<Button-1>", clearField)

scoreLeftEntry = AutocompleteEntry(top)
scoreLeftEntry.grid(row = 3, column = 1)
#scoreLeftEntry.bind("<Button-1>", clearField)

scoreRightEntry = AutocompleteEntry(top)
scoreRightEntry.grid(row = 4, column = 1)
#scoreRightEntry.bind("<Button-1>", clearField)

roundEntry = AutocompleteEntry(top)
roundEntry.set_completion_list(rounds)
roundEntry.grid(row = 5, column = 1)
#roundEntry.bind("<Button-1>", clearField)

commentary1Entry = AutocompleteEntry(top)
#commentary1Entry.set_completion_list(nameData)
commentary1Entry.grid(row = 6, column = 1)
#commentary1Entry.bind("<Button-1>", clearField)

commentary2Entry = AutocompleteEntry(top)
#commentary2Entry.set_completion_list(nameData)
commentary2Entry.grid(row = 7, column = 1)
#commentary2Entry.bind("<Button-1>", clearField)

socPlayerLeftEntry = AutocompleteEntry(top)
#socPlayerLeftEntry.set_completion_list(nameData)
socPlayerLeftEntry.grid(row = 1, column = 3)
#socPlayerLeftEntry.bind("<Button-1>", clearField)

socPlayerRightEntry = AutocompleteEntry(top)
#socPlayerRightEntry.set_completion_list(nameData)
socPlayerRightEntry.grid(row = 2, column = 3)
#socPlayerRightEntry.bind("<Button-1>", clearField)

socCommentary1Entry = AutocompleteEntry(top)
#socCommentary1Entry.set_completion_list(nameData)
socCommentary1Entry.grid(row = 6, column = 3)
#socCommentary1Entry.bind("<Button-1>", clearField)

socCommentary2Entry = AutocompleteEntry(top)
#socCommentary2Entry.set_completion_list(nameData)
socCommentary2Entry.grid(row = 7, column = 3)
#socCommentary2Entry.bind("<Button-1>", clearField)

#listboxes
gamebox = Listbox(top, height = 2, exportselection = False)
gamebox.grid(row = 0, column = 1)
gamebox.insert(END, 'Melee')
gamebox.insert(END, 'Sm4sh')

colors = ['red', 'blue', 'white', 'black', 'green']
colorBoxLeft = Listbox(top, height = 5, exportselection = False)
for color in colors:
        colorBoxLeft.insert(END, color)
colorBoxLeft.grid(row = 1, column = 5)

colors = ['red', 'blue', 'white', 'black', 'green']
colorBoxRight = Listbox(top, height = 5, exportselection = False)
for color in colors:
        colorBoxRight.insert(END, color)
colorBoxRight.grid(row = 2, column = 5)


#buttons
updateButton = Button(top, text = 'Update', command = update)
updateButton.grid(row = 8, column = 0)

#resetButton = Button(top, text = 'Reset', command = resetXMLB)
#resetButton.grid(row = 8, column = 1)

#addSMButton = Button(top, text = 'Add Social Media', command = addSM)
#addSMButton.grid(row = 8, column = 2)

switchLeftRightButton = Button(top, text = 'Switch Left and Right', command = switchLeftRight).grid(row = 8, column = 3)

#loop
top.mainloop()
