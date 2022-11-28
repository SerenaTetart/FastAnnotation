from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import ttk
import tkinter as tk
import pandas as pd
import numpy as np
import PIL
import os

import xml.etree.ElementTree as gfg

RANGERESIZE = 10 #global const variable

def IsFileImage(fileName):
    listTypes = ('jpg', 'jpeg', 'png', 'bmp', 'jfif')
    for types in listTypes:
        if(types in fileName or types.upper() in fileName): return True
    return False

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.IndexPhoto = 0
        self.IsDrawingBB = False
        self.IsDrawingKP = -1
        self.ListFile = []
        self.WorkingDir = os.getcwd()
        boolTmp = False
        boolTmp2 = False
        for file in os.listdir(os.getcwd()):
            if(file == 'boundingBoxes.csv'):
                self.dataBB = pd.read_csv('boundingBoxes.csv')
                boolTmp = True
            elif(file == 'keyPoints.csv'):
                self.dataKP = pd.read_csv('keyPoints.csv')
                boolTmp2 = True
        if(not boolTmp):
            self.dataBB = pd.DataFrame(columns=['image_id', 'width', 'height', 'class', 'x', 'y', 'w', 'h'])
        if(not boolTmp2):
            self.dataKP = pd.DataFrame(columns=['image_id', 'width', 'height', 'key_point', 'x', 'y'])
        self.tmpBB = [(-1, -1), (-1, -1)]; self.ListRect = []
        self.iconDir = tk.PhotoImage(file='icons/directoryIcon.png')
        self.iconDustbin = tk.PhotoImage(file='icons/dustbin.png')
        self.colorList = ['red', 'blue', 'orange', 'purple', 'brown', 'green', 'pink', 'teal', 'yellow', 'grey']
        self.selectedRect = 0
        self.selectedCross = -1
        self.listKP = []
        
        self.resizable(False,False)
        self.title('FastAnnotation 0.4')
        self.protocol("WM_DELETE_WINDOW", self.quit_Button)
        self.geometry('960x540')
        
         # Widgets
        self.PhotoCanvas = tk.Canvas(self, width=960, height=540, bg='grey')
        self.PhotoCanvas.pack(fill="both", expand=True)
        self.rightClickMenu = tk.Menu(self, tearoff=0)
        self.rightClickMenu.add_command(label = "Change class", command=self.chClassBB)
        self.rightClickMenu.add_command(label = "Delete", command=self.deleteBB)
        
        if(len(self.ListFile) > 0): self.showImage()
        self.open_PanelTab()
        self.bind('<Left>', self.leftArrow) #Left Arrow
        self.bind('<Right>', self.rightArrow)
        self.bind('<Return>', self.enterKey)
        self.bind("<ButtonPress-1>", self.leftClick)
        self.bind("<ButtonRelease-1>", self.leftClickRelease)
        self.bind("<ButtonPress-3>", self.rightClick)
        self.bind("<B1-Motion>", self.dragClick)
       
    def quit_Button(self):
        self.destroy()
            
      #Panel Tab
           
    def open_PanelTab(self):
        global panelTab
        global classEntry
        global workingDirEntry
        global tab2
        try:
            if(panelTab.state() == "normal"): panelTab.focus()
        except:
            panelTab = tk.Toplevel(self)
            panelTab.title('Panel Tab')
            panelTab.resizable(False,False)
            
              # Tabs
            tabControl = ttk.Notebook(panelTab)
            tab1 = ttk.Frame(tabControl)
            tab2 = ttk.Frame(tabControl)
            tabControl.pack(expand = 1, fill ="both")
            tabControl.add(tab1, text='Bounding box')
            tabControl.add(tab2, text='Key points')
            
            
            #=== Bounding boxes ===#
             # Widgets
            workingDirButton = tk.Button(tab1, image=self.iconDir, command=lambda: self.selectWorkingDir(), padx=5, pady=5)
            workingDirEntry = tk.Entry(tab1, state='disabled', width = 22)
            classLabel = tk.Label(tab1, text="Object class:")
            classEntry = tk.Entry(tab1, width = 22)
            lastImage_Button = tk.Button(tab1, text='<-', command=lambda: self.showLastImage(), padx=5, pady=5)
            deleteImage_Button = tk.Button(tab1, text='Del', bg='red', command=lambda: self.deleteImage(), padx=5, pady=5)
            nextImage_Button = tk.Button(tab1, text='->', command=lambda: self.showNextImage(), padx=5, pady=5)
            photoLabel = tk.Label(tab1, text="Photo Navigation")
            DrawBB_Button = tk.Button(tab1, text='Draw BB', command=lambda: self.toggleDrawBB(), padx=5, pady=5)
            ResetBB_Button = tk.Button(tab1, text='Reset BB', command=lambda: self.resetBB(), padx=5, pady=5)
            Validate_Button = tk.Button(tab1, text='Validate', command=lambda: self.validateBB(), padx=5, pady=5)
            
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
            
            #=== Key points ===#
              # Widgets - Key points
            newKP_Button = tk.Button(tab2, text='New key-point', command=lambda: self.addKP(), padx=5, pady=5)
            affKP_Button = tk.Button(tab2, text='Affect key-points', command=lambda: self.toggleDrawKP(), padx=5, pady=5)
            
              # Grid
            newKP_Button.grid(row=0, column=0, padx=6, pady=5)
            affKP_Button.grid(row=0, column=1, columnspan=2, padx=6, pady=5)
            
            panelTab.attributes('-topmost', True)
            
    def addKP(self):
        self.listKP.append([[-1, -1], tk.Entry(tab2, state='normal', width = 14), tk.Entry(tab2, state='normal', width = 10), tk.Button(tab2, image=self.iconDustbin, command=lambda x=len(self.listKP): self.delKP(x)), 0])
        self.listKP[len(self.listKP)-1][2].insert(0, "(-1, -1)")
        self.listKP[len(self.listKP)-1][2].configure(state='disabled')
        self.listKP[len(self.listKP)-1][1].grid(row=1+(len(self.listKP)-1)%5+(((len(self.listKP)-1)//20)*5), column=0+(((len(self.listKP)-1)//5)*3)%12)
        self.listKP[len(self.listKP)-1][2].grid(row=1+(len(self.listKP)-1)%5+(((len(self.listKP)-1)//20)*5), column=1+(((len(self.listKP)-1)//5)*3)%12)
        self.listKP[len(self.listKP)-1][3].grid(row=1+(len(self.listKP)-1)%5+(((len(self.listKP)-1)//20)*5), column=2+(((len(self.listKP)-1)//5)*3)%12)
            
    def delKP(self, index):
        self.listKP[index][1].grid_remove()
        self.listKP[index][2].grid_remove()
        self.listKP[index][3].grid_remove()
        if(self.listKP[index][4] != 0):
            self.PhotoCanvas.delete(self.listKP[index][4][0])
            self.PhotoCanvas.delete(self.listKP[index][4][1])
            self.PhotoCanvas.delete(self.listKP[index][4][2])
        self.listKP.pop(index)
        for i in range(index, len(self.listKP)):
            self.listKP[i][3].configure(command=lambda x=i: self.delKP(x))
            self.listKP[i][1].grid(row=1+(i%5)+((i//20)*5), column=0+((i//5)*3)%12)
            self.listKP[i][2].grid(row=1+(i%5)+((i//20)*5), column=1+((i//5)*3)%12)
            self.listKP[i][3].grid(row=1+(i%5)+((i//20)*5), column=2+((i//5)*3)%12)
            
    def selectWorkingDir(self):
        if(self.IsDrawingBB): self.toggleDrawBB()
        tmp = filedialog.askdirectory(title='Select your working directory', initialdir=self.WorkingDir)
        if(tmp != ""):
            self.resetBB()
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
        if(not self.IsDrawingBB):
            if(self.IsDrawingKP > 0): self.IsDrawingKP = -1
            objectClass = classEntry.get()
            if(objectClass == ''): messagebox.showerror('Error', 'No class specified !')
            else:
                self.tmpBB = [(-1, -1), (-1, -1)]
                self.IsDrawingBB = True
                self.config(cursor="cross")
                panelTab.config(cursor="cross")
        else:
            self.IsDrawingBB = False
            self.IsDrawingKP = -1
            self.config(cursor="arrow")
            panelTab.config(cursor="arrow")
            
    def toggleDrawKP(self):
        if(self.IsDrawingKP == -1):
            if(self.IsDrawingBB): self.IsDrawingBB = False
            okB = True
            for i in range(len(self.listKP)):
                if(self.listKP[i][1].get() == ""):
                    messagebox.showerror('Error', 'No name specified for key-point ' + str(i) + ' !')
                    okB = False
                    break
            if(okB):
                for i in range(len(self.listKP)):
                    if(self.listKP[i][0][0] == -1 or self.listKP[i][0][1] == -1):
                        self.IsDrawingKP = i
                        self.config(cursor="cross")
                        panelTab.config(cursor="cross")
                        return
                if(len(self.ListFile) > 0): self.GenerateCSV_KP()
        else:
            self.IsDrawingBB = False
            self.IsDrawingKP = -1
            self.config(cursor="arrow")
            panelTab.config(cursor="arrow")
            if(len(self.ListFile) > 0): self.GenerateCSV_KP()
         
    def rightClick(self, event):
        self.selectedRect = [0, 0]
        x, y = event.x, event.y
            #Select BB
        if(not self.IsDrawingBB):
            for rect in self.ListRect:
                x0, y0, x1, y1 = self.PhotoCanvas.coords(rect[0])
                if(x > x0 and x < x1 and y > y0 and y < y1):
                    self.selectedRect = rect
                    self.PhotoCanvas.focus(rect[0])
                    try:
                        self.rightClickMenu.tk_popup(self.winfo_rootx()+x+15, self.winfo_rooty()+y-5)
                    finally:
                        self.rightClickMenu.grab_release()
                    break
         
    def leftClick(self, event):
        global RANGERESIZE
        self.selectedRect = [0, 0]
        self.selectedCross = -1
        x, y = event.x, event.y #Mouse coord
        self.posx = x; self.posy = y
            #Select BB
        if(not self.IsDrawingBB and self.IsDrawingKP == -1):
            for i in range(len(self.listKP)):
                x0, y0 = self.listKP[i][0]
                if(x >= x0-RANGERESIZE and x <= x0+RANGERESIZE and y >= y0-RANGERESIZE and y <= y0+RANGERESIZE):
                    self.config(cursor="fleur")
                    self.selectedCross = i
            for rect in self.ListRect:
                x0, y0, x1, y1 = self.PhotoCanvas.coords(rect[0])
                if(x >= x0 and x <= x1 and y >= y0 and y <= y1):
                    if(y <= y0+RANGERESIZE or y >= y1-RANGERESIZE): self.config(cursor="sb_v_double_arrow")
                    elif(x <= x0+RANGERESIZE or x >= x1-RANGERESIZE): self.config(cursor="sb_h_double_arrow")
                    else: self.config(cursor="fleur")
                    self.selectedRect = rect
                    self.PhotoCanvas.focus(rect[0])
                    self.PhotoCanvas.focus(rect[1])
                    break
            #Draw BB
        elif(self.IsDrawingBB):
            objectClass = classEntry.get()
            if(self.tmpBB[0] == (-1, -1)):
                self.tmpBB[0] = (x, y)
            elif(self.tmpBB[1] == (-1, -1)):
                self.tmpBB[1] = (x, y)
                self.toggleDrawBB() #Stop drawing
                rect = self.PhotoCanvas.create_rectangle(
                    self.tmpBB[0][0], self.tmpBB[0][1],
                    self.tmpBB[1][0], self.tmpBB[1][1], width=2,
                    outline='black', tags=objectClass)
                text = self.PhotoCanvas.create_text(self.tmpBB[1][0] - 15, self.tmpBB[1][1] + 5, text=objectClass, font=("Arial", 10), fill='black')
                self.ListRect.append([rect, text])
            #Draw KP
        elif(self.IsDrawingKP > -1):
            if(self.listKP[self.IsDrawingKP][4] != 0):
                self.PhotoCanvas.delete(self.listKP[self.IsDrawingKP][4][0])
                self.PhotoCanvas.delete(self.listKP[self.IsDrawingKP][4][1])
                self.PhotoCanvas.delete(self.listKP[self.IsDrawingKP][4][2])
            self.listKP[self.IsDrawingKP][4] = [self.PhotoCanvas.create_line(x+5, y+5, x-5, y-5, fill="green", width="2"),
                self.PhotoCanvas.create_line(x+5, y-5, x-5, y+5, fill="green", width="2"),
                self.PhotoCanvas.create_text(x, y+10, text=self.listKP[self.IsDrawingKP][1].get(), font=("Arial", 10), fill='green')]
            self.listKP[self.IsDrawingKP][0] = [x, y]
            self.listKP[self.IsDrawingKP][2].configure(state='normal')
            self.listKP[self.IsDrawingKP][2].delete(0,tk.END)
            self.listKP[self.IsDrawingKP][2].insert(0, "("+str(x)+", "+str(y)+")")
            self.listKP[self.IsDrawingKP][2].configure(state='disabled')
            for i in range(len(self.listKP)):
                if(self.listKP[i][0][0] == -1 or self.listKP[i][0][1] == -1):
                    self.IsDrawingKP = i
                    return
            self.toggleDrawKP()
                
    def leftClickRelease(self, event):
        if(not self.IsDrawingBB and self.IsDrawingKP == -1): self.config(cursor="arrow")
                
    def dragClick(self, event):
        global RANGERESIZE
        if(not self.IsDrawingBB and self.IsDrawingKP == -1 and self.selectedCross != -1):
            x, y = event.x, event.y
            distx = x - self.posx; disty = y - self.posy
            x00, y00, x01, y01 = self.PhotoCanvas.coords(self.listKP[self.selectedCross][4][0])
            x10, y10, x11, y11 = self.PhotoCanvas.coords(self.listKP[self.selectedCross][4][1])
            x2, y2 = self.PhotoCanvas.coords(self.listKP[self.selectedCross][4][2])
            self.PhotoCanvas.coords(self.listKP[self.selectedCross][4][0], x00+distx, y00+disty, x01+distx, y01+disty)
            self.PhotoCanvas.coords(self.listKP[self.selectedCross][4][1], x10+distx, y10+disty, x11+distx, y11+disty)
            self.PhotoCanvas.coords(self.listKP[self.selectedCross][4][2], x2+distx, y2+disty)
            self.listKP[self.selectedCross][0] = [x, y]
            self.listKP[self.selectedCross][2].configure(state='normal')
            self.listKP[self.selectedCross][2].delete(0,tk.END)
            self.listKP[self.selectedCross][2].insert(0, "("+str(x)+", "+str(y)+")")
            self.listKP[self.selectedCross][2].configure(state='disabled')
            self.posx = x; self.posy = y
        elif(not self.IsDrawingBB and self.IsDrawingKP == -1 and self.selectedRect[0] != 0):
            x, y = event.x, event.y
            distx = x - self.posx; disty = y - self.posy
            x0, y0, x1, y1 = self.PhotoCanvas.coords(self.selectedRect[0])
            x2, y2 = self.PhotoCanvas.coords(self.selectedRect[1])
            if(self.posx >= x0 and self.posx <= x1 and self.posy >= y0 and self.posy <= y0+RANGERESIZE):
                self.PhotoCanvas.coords(self.selectedRect[0], x0, y0+disty, x1, y1)
                self.PhotoCanvas.coords(self.selectedRect[1], x2, y2)
            elif(self.posx >= x0 and self.posx <= x1 and self.posy >= y1-RANGERESIZE and self.posy <= y1):
                self.PhotoCanvas.coords(self.selectedRect[0], x0, y0, x1, y1+disty)
                self.PhotoCanvas.coords(self.selectedRect[1], x2, y2+disty)
            elif(self.posx >= x0 and self.posx <= x0+RANGERESIZE and self.posy >= y0 and self.posy <= y1):
                self.PhotoCanvas.coords(self.selectedRect[0], x0+distx, y0, x1, y1)
                self.PhotoCanvas.coords(self.selectedRect[1], x2, y2)
            elif(self.posx >= x1-RANGERESIZE and self.posx <= x1 and self.posy >= y0 and self.posy <= y1):
                self.PhotoCanvas.coords(self.selectedRect[0], x0, y0, x1+distx, y1)
                self.PhotoCanvas.coords(self.selectedRect[1], x2+distx, y2)
            else:
                self.PhotoCanvas.coords(self.selectedRect[0], x0+distx, y0+disty, x1+distx, y1+disty)
                self.PhotoCanvas.coords(self.selectedRect[1], x2+distx, y2+disty)
            self.posx = x; self.posy = y
            
    def resetBB(self):
        for rect in self.ListRect:
            self.PhotoCanvas.delete(rect[0])
            self.PhotoCanvas.delete(rect[1])
        self.ListRect = []
        
    def deleteBB(self):
        if(self.selectedRect[0] > 0):
            self.PhotoCanvas.delete(self.selectedRect[0])
            self.PhotoCanvas.delete(self.selectedRect[1])
            self.ListRect.remove(self.selectedRect)
          
    def chClassBB(self):
        if(self.selectedRect[0] > 0):
            objectClass = classEntry.get()
            if(objectClass == ''): messagebox.showerror('Error', 'No class specified !')
            else:
                self.PhotoCanvas.itemconfig(self.selectedRect[0], tag=objectClass)
                self.PhotoCanvas.itemconfig(self.selectedRect[0], outline='black')
                self.PhotoCanvas.itemconfig(self.selectedRect[1], text=objectClass)
                self.PhotoCanvas.itemconfig(self.selectedRect[1], fill='black')
        
    def leftArrow(self, event):
        self.showLastImage()
        
    def rightArrow(self, event):
        self.showNextImage()
        
    def enterKey(self, event):
        self.validateBB()
        if(len(self.ListFile) > 0): self.GenerateCSV_KP()
        
    def validateBB(self):
        if(len(self.ListFile) > 0):
            self.GenerateCSV_BB()
            self.GenerateXML()
            self.showNextImage()
            
    def GenerateCSV_BB(self):
        ''' Generate the CSV file associated to the set of images worked on '''
        selection = self.dataBB[self.dataBB['image_id'] == self.ListFile[self.IndexPhoto]].index
        self.dataBB.drop(selection, inplace=True)
        fileShape = np.array(Image.open(self.WorkingDir+'/'+self.ListFile[self.IndexPhoto])).shape
        for rect in self.ListRect:
            x0, y0, x1, y1 = self.PhotoCanvas.coords(rect[0])
            objectClass = self.PhotoCanvas.gettags(rect[0])
            new_row = {'image_id':self.ListFile[self.IndexPhoto],
                'width':fileShape[1],
                'height':fileShape[0],
                'class':objectClass[0],
                'x':x0, 'y':y0, 'w':x1-x0, 'h':y1-y0} 
            self.dataBB = self.dataBB.append(new_row, ignore_index=True)
        self.dataBB.to_csv (os.getcwd()+'/boundingBoxes.csv', index = False, header=True)
        
    def GenerateCSV_KP(self):
        ''' Generate the CSV file associated to the set of images worked on '''
        selection = self.dataKP[self.dataKP['image_id'] == self.ListFile[self.IndexPhoto]].index
        self.dataKP.drop(selection, inplace=True)
        fileShape = np.array(Image.open(self.WorkingDir+'/'+self.ListFile[self.IndexPhoto])).shape
        for KP in self.listKP:
            x, y = KP[0]
            name = KP[1].get()
            new_row = {'image_id':self.ListFile[self.IndexPhoto],
                'width':fileShape[1],
                'height':fileShape[0],
                'key_point':name, 'x':x, 'y':y}
            self.dataKP = self.dataKP.append(new_row, ignore_index=True)
        self.dataKP.to_csv (os.getcwd()+'/keyPoints.csv', index = False, header=True)
            
    def GenerateXML(self):
        ''' Generate the XML file associated to the image worked on '''
        if(not os.path.exists(os.getcwd()+'/PascalVOC_XML')): os.mkdir(os.getcwd()+'/PascalVOC_XML')
        root = gfg.Element("annotation")
        dirTmp = self.WorkingDir[self.WorkingDir.rfind('/')+1::]
        b1 = gfg.SubElement(root, "folder")
        b1.text = dirTmp
        b2 = gfg.SubElement(root, "filename")
        b2.text = self.ListFile[self.IndexPhoto][:-4]
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
        
        for rect in self.ListRect:
            x0, y0, x1, y1 = self.PhotoCanvas.coords(rect[0])
            objectClass = self.PhotoCanvas.gettags(rect[0])
            m = gfg.Element("object")
            root.append(m)
            e1 = gfg.SubElement(m, "name")
            e1.text = objectClass[0]
            e2 = gfg.SubElement(m, "pose")
            e2.text = 'Unspecified'
            e3 = gfg.SubElement(m, "truncated")
            e3.text = '0'
            e4 = gfg.SubElement(m, "difficult")
            e4.text = '0'
            n = gfg.Element("bndbox")
            m.append(n)
            f1 = gfg.SubElement(n, "xmin")
            f1.text = str(int(x0))
            f2 = gfg.SubElement(n, "ymin")
            f2.text = str(int(y0))
            f3 = gfg.SubElement(n, "xmax")
            f3.text = str(int(x1))
            f4 = gfg.SubElement(n, "ymax")
            f4.text = str(int(y1))
            
        tree = gfg.ElementTree(root)
        with open (os.getcwd()+'/PascalVOC_XML/'+self.ListFile[self.IndexPhoto][:-4]+'.xml', "wb") as files :
            tree.write(files)
            
    def showImage(self):
        img = Image.open(self.WorkingDir+'/'+self.ListFile[self.IndexPhoto])
        self.geometry(str(img.size[0])+'x'+str(img.size[1]))
        self.displayedIMG = ImageTk.PhotoImage(image=img)
        self.PhotoCanvas.create_image((0, 0), anchor=tk.NW, image=self.displayedIMG)
            #Bounding boxes
        selection_BB = self.dataBB[self.dataBB['image_id'] == self.ListFile[self.IndexPhoto]]
        listClass = self.dataBB['class'].unique()
        for index, row in selection_BB.iterrows():
            colorIndex = 0; color = 'black'
            for classLabel in listClass:
                if(row['class'] == classLabel):
                    color = self.colorList[colorIndex]
                    break
                else: colorIndex += 1
            x0, y0, x1, y1 = row['x'], row['y'], (row['w'] + row['x']), (row['h'] + row['y'])
            rect = self.PhotoCanvas.create_rectangle(
                x0, y0, x1, y1, width=2,
                outline=color, tags=row['class'])
            text = self.PhotoCanvas.create_text(x1 - 15, y1 + 7, text=row['class'], font=("Arial", 10), fill=color)
            self.ListRect.append([rect, text])
            #Key points
        selection_KP = self.dataKP[self.dataKP['image_id'] == self.ListFile[self.IndexPhoto]]
        for i in range(len(self.listKP)):
            self.listKP[i][0][0] = -1
            self.listKP[i][0][1] = -1
            self.listKP[i][2].configure(state='normal')
            self.listKP[i][2].delete(0,tk.END)
            self.listKP[i][2].insert(0, "(-1, -1)")
            self.listKP[i][2].configure(state='disabled')
            if(self.listKP[i][4] != 0):
                self.PhotoCanvas.delete(self.listKP[i][4][0])
                self.PhotoCanvas.delete(self.listKP[i][4][1])
                self.PhotoCanvas.delete(self.listKP[i][4][2])
                self.listKP[i][4] = 0
        i = 0
        for index, row in selection_KP.iterrows():
            if(len(self.listKP) < i+1): self.addKP()
            x, y = row['x'], row['y']
            name = row['key_point']
            self.listKP[i][0][0] = x
            self.listKP[i][0][1] = y
            self.listKP[i][4] = [self.PhotoCanvas.create_line(x+5, y+5, x-5, y-5, fill="green", width="2"),
                self.PhotoCanvas.create_line(x+5, y-5, x-5, y+5, fill="green", width="2"),
                self.PhotoCanvas.create_text(x, y+10, text=name, font=("Arial", 10), fill='green')]
            self.listKP[i][0] = [x, y]
            self.listKP[i][1].delete(0,tk.END)
            self.listKP[i][1].insert(0, name)
            self.listKP[i][2].configure(state='normal')
            self.listKP[i][2].delete(0,tk.END)
            self.listKP[i][2].insert(0, "("+str(x)+", "+str(y)+")")
            self.listKP[i][2].configure(state='disabled')
            i += 1
            
    def showNextImage(self):
        if(len(self.ListFile) > 0):
            if(self.IsDrawingBB): self.toggleDrawBB() #Stop drawing
            self.resetBB() #Reset all bounding boxes
            if(self.IndexPhoto+1 >= len(self.ListFile)): self.IndexPhoto = 0
            else: self.IndexPhoto += 1
            self.showImage()
            
    def showLastImage(self):
        if(len(self.ListFile) > 0):
            if(self.IsDrawingBB): self.toggleDrawBB()
            self.resetBB()
            if(self.IndexPhoto-1 < 0): self.IndexPhoto = len(self.ListFile)-1
            else: self.IndexPhoto -= 1
            self.showImage()
            
    def deleteImage(self):
        if(len(self.ListFile) > 0):
            if(self.IsDrawingBB): self.toggleDrawBB()
            self.resetBB()
            selection = self.dataBB[self.dataBB['image_id'] == self.ListFile[self.IndexPhoto]].index
            self.dataBB.drop(selection, inplace=True)
            self.dataBB.to_csv (os.getcwd()+'/boundingBoxes.csv', index = False, header=True)
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