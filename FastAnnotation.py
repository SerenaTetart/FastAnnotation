from tkinter import messagebox
from PIL import ImageTk, Image
import tkinter as tk
import pandas as pd
import numpy as np
import PIL
import os

PATH_ANNOTATION = os.getcwd()

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.IndexPhoto = 0
        self.IsDrawing = False
        self.ListFile = []
        if(not os.path.exists(PATH_ANNOTATION+'/RawData')): os.mkdir(PATH_ANNOTATION+'/RawData')
        for file in os.listdir(PATH_ANNOTATION+'/RawData/'):
            self.ListFile.append(file)
        boolTmp = False
        for file in os.listdir(PATH_ANNOTATION):
            if(file == 'annotations.csv'):
                self.dataBB = pd.read_csv('annotations.csv')
                boolTmp = True
        if(not boolTmp):
            self.dataBB = pd.DataFrame(columns=['image', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
        self.tmpBB = [(-1, -1), (-1, -1)]
        self.ListBB = []
        self.ListRect = []
        self.colorList = ['red', 'blue', 'green', 'yellow', 'brown', 'grey', 'purple', 'pink', 'orange', 'teal']
        
        self.resizable(False,False)
        self.title('FastAnnotation 0.1')
        self.protocol("WM_DELETE_WINDOW", self.quit_Button)
        self.geometry('960x540')
         # Widgets
        self.PhotoCanvas = tk.Canvas(self, width=960, height=540, bg='grey')
         # Grid
        self.PhotoCanvas.pack(fill="both", expand=True)
        
        if(len(self.ListFile) > 0): self.showImage()
        
        self.open_PanelTab()
        self.bind("<Button-1>", self.drawBB)
       
    def quit_Button(self):
        self.destroy()
            
      #Panel Tab
    def close_PanelTab(self):
        panelTab.destroy()
           
    def open_PanelTab(self):
        global panelTab
        global classEntry
        try:
            if(panelTab.state() == "normal"): panelTab.focus()
        except:
            panelTab = tk.Toplevel(self)
            panelTab.title('Panel Tab')
            panelTab.resizable(False,False)
            
             # Widgets
            classLabel = tk.Label(panelTab, text="Object Class:")
            classEntry = tk.Entry(panelTab, width = 20)
            lastImage_Button = tk.Button(panelTab, text='<-', command=lambda: self.showLastImage(), padx=5, pady=5)
            deleteImage_Button = tk.Button(panelTab, text='Del', bg='red', command=lambda: self.deleteImage(), padx=5, pady=5)
            nextImage_Button = tk.Button(panelTab, text='->', command=lambda: self.showNextImage(), padx=5, pady=5)
            photoLabel = tk.Label(panelTab, text="Photo Navigation")
            DrawBB_Button = tk.Button(panelTab, text='Draw BB', command=lambda: self.toggleDrawBB(), padx=5, pady=5)
            ResetBB_Button = tk.Button(panelTab, text='Reset BB', command=lambda: self.resetBB(), padx=5, pady=5)
            Validate_Button = tk.Button(panelTab, text='Validate', command=lambda: self.validateBB(), padx=5, pady=5)
            
             # Grid
            classLabel.grid(row=0, column=0)
            classEntry.grid(row=0, column=1, columnspan=2)
            DrawBB_Button.grid(row=1, column=0, pady=5)
            ResetBB_Button.grid(row=1, column=1, pady=5)
            Validate_Button.grid(row=1, column=2, pady=5)
            photoLabel.grid(row=2, column=1, pady=5)
            lastImage_Button.grid(row=3, column=0, pady=5)
            deleteImage_Button.grid(row=3, column=1, pady=5)
            nextImage_Button.grid(row=3, column=2, pady=5)
            
            panelTab.attributes('-topmost', True)
            
    def toggleDrawBB(self):
        if(not self.IsDrawing):
            objectClass = classEntry.get()
            if(objectClass == ''): messagebox.showerror('Error', 'No class specified !')
            else:
                self.tmpBB = [(-1, -1), (-1, -1)]
                self.IsDrawing = True
                self.config(cursor="cross")
                panelTab.config(cursor="cross")
        else:
            self.IsDrawing = False
            self.config(cursor="arrow")
            panelTab.config(cursor="arrow")
            
    def drawBB(self, event):
        if(self.IsDrawing):
            objectClass = classEntry.get()
            x, y = event.x, event.y
            if(self.tmpBB[0] == (-1, -1)):
                self.tmpBB[0] = (x, y)
            elif(self.tmpBB[1] == (-1, -1)):
                self.tmpBB[1] = (x, y)
                self.toggleDrawBB() #Stop drawing
                self.tmpBB.append(objectClass)
                self.ListBB.append(self.tmpBB)
                rect = self.PhotoCanvas.create_rectangle(
                    self.tmpBB[0][0], self.tmpBB[0][1],
                    self.tmpBB[1][0], self.tmpBB[1][1], width=2,
                    outline='black')
                self.ListRect.append(rect)
            
    def resetBB(self):
        self.ListBB = []
        for rect in self.ListRect:
            self.PhotoCanvas.delete(rect)
        self.ListRect = []
        
    def validateBB(self):
        if(len(self.ListFile) > 0):
            selection = self.dataBB[self.dataBB['image'] == self.ListFile[self.IndexPhoto]].index
            self.dataBB.drop(selection, inplace=True)
            for BB in self.ListBB:
                width = abs(BB[0][0] - BB[1][0]) # |xmin - xmax|
                height = abs(BB[0][1] - BB[1][1]) # |ymin - ymax|
                new_row = {'image':self.ListFile[self.IndexPhoto],
                        'width':width,
                        'height':height,
                        'class':BB[2],
                        'xmin':BB[0][0], 'ymin':BB[0][1],
                        'xmax':BB[1][0], 'ymax':BB[1][1]}
                self.dataBB = self.dataBB.append(new_row, ignore_index=True)
            self.dataBB.to_csv (PATH_ANNOTATION+'/annotations.csv', index = False, header=True)
            self.showNextImage()
            
    def showImage(self):
        img = Image.open(PATH_ANNOTATION+'/RawData/'+self.ListFile[self.IndexPhoto])
        self.geometry(str(img.size[0])+'x'+str(img.size[1]))
        self.displayedIMG = ImageTk.PhotoImage(image=img)
        self.PhotoCanvas.create_image((0, 0), anchor=tk.NW, image=self.displayedIMG)
        selection = self.dataBB[self.dataBB['image'] == self.ListFile[self.IndexPhoto]]
        listClass = self.dataBB['class'].unique()
        for index, row in selection.iterrows():
            colorIndex = 0; color = 'black'
            for classLabel in listClass:
                if(row['class'] == classLabel):
                    color = self.colorList[colorIndex]
                    break
                else: colorIndex += 1
            rect = self.PhotoCanvas.create_rectangle(
                row['xmin'], row['ymin'],
                row['xmax'], row['ymax'], width=2,
                outline=color)
            self.ListRect.append(rect)
            self.ListBB.append([(row['xmin'], row['ymin']), (row['xmax'], row['ymax']), row['class']])
            
    def showNextImage(self):
        if(len(self.ListFile) > 0):
            if(self.IsDrawing): self.toggleDrawBB() #Stop drawing
            self.resetBB() #Reset all bounding boxes
            if(self.IndexPhoto+1 >= len(self.ListFile)): self.IndexPhoto = 0
            else: self.IndexPhoto += 1
            self.showImage()
            
    def showLastImage(self):
        if(len(self.ListFile) > 0):
            if(self.IsDrawing): self.toggleDrawBB()
            self.resetBB()
            if(self.IndexPhoto-1 < 0): self.IndexPhoto = len(self.ListFile)-1
            else: self.IndexPhoto -= 1
            self.showImage()
            
    def deleteImage(self):
        if(len(self.ListFile) > 0):
            if(self.IsDrawing): self.toggleDrawBB()
            self.resetBB()
            selection = self.dataBB[self.dataBB['image'] == self.ListFile[self.IndexPhoto]].index
            self.dataBB.drop(selection, inplace=True)
            self.dataBB.to_csv (PATH_ANNOTATION+'/annotations.csv', index = False, header=True)
            os.remove(PATH_ANNOTATION+'/RawData/'+self.ListFile[self.IndexPhoto])
            self.ListFile = []
            for file in os.listdir(PATH_ANNOTATION+'/RawData/'):
                self.ListFile.append(file)
            if(self.IndexPhoto > len(self.ListFile)-1): self.IndexPhoto = 0
            if(len(self.ListFile) > 0): self.showImage()
            else: self.PhotoCanvas.delete('all')
        
    #Main :
if __name__== "__main__" :
    interface = Interface()
    interface.mainloop()