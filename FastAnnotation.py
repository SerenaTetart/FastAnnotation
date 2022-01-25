from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import tkinter as tk
import pandas as pd
import numpy as np
import PIL
import os

import xml.etree.ElementTree as gfg

def IsFileImage(fileName):
    listTypes = ('jpg', 'png', 'bmp')
    for types in listTypes:
        if(types in fileName or types.upper() in fileName): return True
    return False

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.IndexPhoto = 0
        self.IsDrawing = False
        self.ListFile = []
        self.WorkingDir = os.getcwd()
        boolTmp = False
        for file in os.listdir(os.getcwd()):
            if(file == 'annotations.csv'):
                self.dataBB = pd.read_csv('annotations.csv')
                boolTmp = True
        if(not boolTmp):
            self.dataBB = pd.DataFrame(columns=['image', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])
        self.tmpBB = [(-1, -1), (-1, -1)]; self.ListBB = []; self.ListRect = []
        self.iconDir = tk.PhotoImage(file='icons/directoryIcon.png')
        self.colorList = ['red', 'blue', 'green', 'yellow', 'brown', 'grey', 'purple', 'pink', 'orange', 'teal']
        
        self.resizable(False,False)
        self.title('FastAnnotation 0.2')
        self.protocol("WM_DELETE_WINDOW", self.quit_Button)
        self.geometry('960x540')
        
         # Widgets
        self.PhotoCanvas = tk.Canvas(self, width=960, height=540, bg='grey')
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
        global workingDirEntry
        try:
            if(panelTab.state() == "normal"): panelTab.focus()
        except:
            panelTab = tk.Toplevel(self)
            panelTab.title('Panel Tab')
            panelTab.resizable(False,False)
            
             # Widgets
            workingDirButton = tk.Button(panelTab, image=self.iconDir, command=lambda: self.selectWorkingDir(), padx=5, pady=5)
            workingDirEntry = tk.Entry(panelTab, state='disabled', width = 22)
            classLabel = tk.Label(panelTab, text="Object class:")
            classEntry = tk.Entry(panelTab, width = 22)
            lastImage_Button = tk.Button(panelTab, text='<-', command=lambda: self.showLastImage(), padx=5, pady=5)
            deleteImage_Button = tk.Button(panelTab, text='Del', bg='red', command=lambda: self.deleteImage(), padx=5, pady=5)
            nextImage_Button = tk.Button(panelTab, text='->', command=lambda: self.showNextImage(), padx=5, pady=5)
            photoLabel = tk.Label(panelTab, text="Photo Navigation")
            DrawBB_Button = tk.Button(panelTab, text='Draw BB', command=lambda: self.toggleDrawBB(), padx=5, pady=5)
            ResetBB_Button = tk.Button(panelTab, text='Reset BB', command=lambda: self.resetBB(), padx=5, pady=5)
            Validate_Button = tk.Button(panelTab, text='Validate', command=lambda: self.validateBB(), padx=5, pady=5)
            
             # Grid
            workingDirButton.grid(row=0, column=0)
            workingDirEntry.grid(row=0, column=1, columnspan=2)
            classLabel.grid(row=1, column=0)
            classEntry.grid(row=1, column=1, columnspan=2)
            DrawBB_Button.grid(row=2, column=0, pady=5)
            ResetBB_Button.grid(row=2, column=1, pady=5)
            Validate_Button.grid(row=2, column=2, pady=5)
            photoLabel.grid(row=3, column=1, pady=5)
            lastImage_Button.grid(row=4, column=0, pady=5)
            deleteImage_Button.grid(row=4, column=1, pady=5)
            nextImage_Button.grid(row=4, column=2, pady=5)
            
            panelTab.attributes('-topmost', True)
            
    def selectWorkingDir(self):
        if(self.IsDrawing): self.toggleDrawBB()
        self.resetBB()
        tmp = filedialog.askdirectory(title='Select your working directory', initialdir=self.WorkingDir)
        if(tmp != ""):
            self.WorkingDir = tmp
            workingDirEntry.configure(state='normal')
            workingDirEntry.delete(0,tk.END)
            workingDirEntry.insert(0,self.WorkingDir)
            workingDirEntry.configure(state='disabled')
            self.ListFile = []
            for file in os.listdir(self.WorkingDir):
                if(IsFileImage(file)): self.ListFile.append(file)
            if(len(self.ListFile) > 0): self.showImage()
            
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
            self.GenerateCSV()
            self.GenerateXML()
            self.showNextImage()
            
    def GenerateCSV(self):
        ''' Generate the CSV file associated to the set of images worked on '''
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
        self.dataBB.to_csv (os.getcwd()+'/annotations.csv', index = False, header=True)
            
    def GenerateXML(self):
        ''' Generate the XML file associated to the image worked on '''
        if(not os.path.exists(os.getcwd()+'/XML_Data')): os.mkdir(os.getcwd()+'/XML_Data')
        root = gfg.Element("annotation")
        dirTmp = self.WorkingDir[self.WorkingDir.rfind('/')+1::]
        b1 = gfg.SubElement(root, "folder")
        b1.text = dirTmp
        b2 = gfg.SubElement(root, "filename")
        b2.text = self.ListFile[self.IndexPhoto]
        b3 = gfg.SubElement(root, "path")
        b3.text = self.WorkingDir+'/'+self.ListFile[self.IndexPhoto]
        
        m1 = gfg.Element("source")
        root.append(m1)
        c1 = gfg.SubElement(m1, "database")
        c1.text = 'Unknown'
        
        fileShape = np.array(Image.open(self.WorkingDir+'/'+self.ListFile[self.IndexPhoto])).shape
        m2 = gfg.Element("size")
        root.append(m2)
        d1 = gfg.SubElement(m2, "width")
        d1.text = str(fileShape[1])
        d2 = gfg.SubElement(m2, "height")
        d2.text = str(fileShape[0])
        d2 = gfg.SubElement(m2, "depth")
        d2.text = str(fileShape[2])
        
        b4 = gfg.SubElement(root, "segmented")
        b4.text = '0'
        
        for BB in self.ListBB:
            m = gfg.Element("object")
            root.append(m)
            e1 = gfg.SubElement(m, "name")
            e1.text = BB[2]
            e2 = gfg.SubElement(m, "pose")
            e2.text = 'Unspecified'
            e3 = gfg.SubElement(m, "truncated")
            e3.text = '0'
            e4 = gfg.SubElement(m, "difficult")
            e4.text = '0'
            n = gfg.Element("bndbox")
            m.append(n)
            f1 = gfg.SubElement(n, "xmin")
            f1.text = str(BB[0][0])
            f2 = gfg.SubElement(n, "ymin")
            f2.text = str(BB[0][1])
            f3 = gfg.SubElement(n, "xmax")
            f3.text = str(BB[1][0])
            f4 = gfg.SubElement(n, "ymax")
            f4.text = str(BB[1][1])
            
        tree = gfg.ElementTree(root)
        with open (os.getcwd()+'/XML_Data/'+self.ListFile[self.IndexPhoto]+'.xml', "wb") as files :
            tree.write(files)
            
    def showImage(self):
        img = Image.open(self.WorkingDir+'/'+self.ListFile[self.IndexPhoto])
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
            self.dataBB.to_csv (os.getcwd()+'/annotations.csv', index = False, header=True)
            os.remove(self.WorkingDir+'/'+self.ListFile[self.IndexPhoto])
            self.ListFile = []
            for file in os.listdir(self.WorkingDir):
                if(IsFileImage(file)): self.ListFile.append(file)
            if(self.IndexPhoto > len(self.ListFile)-1): self.IndexPhoto = 0
            if(len(self.ListFile) > 0): self.showImage()
            else:
                self.PhotoCanvas.delete('all')
                self.geometry('960x540')
        
    #Main :
if __name__== "__main__" :
    interface = Interface()
    interface.mainloop()