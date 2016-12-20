from tkinter import *
import csv
import urllib.request
from re import findall
import string


class mergeData:

    def __init__(self,w):
        fR=Frame(w)
        fR.pack(side="right")
        fL=Frame(w)
        fL.pack(side="left")
        Button(fL,text="Load Input CSV File",command=self.loadCSVclicked).grid(row=0,column=0,columnspan=2,sticky=EW)
        Label(fL,text="File Path").grid(row=1,column=0,columnspan=2,sticky=EW)
        Label(fL,text="Input CSV File").grid(row=2,column=0)
        Label(fL,text="Website URL").grid(row=3,column=0)
        Label(fL,text="Output CSV File").grid(row=4,column=0)
        self.e1=StringVar()
        self.e2=StringVar()
        self.e3=StringVar()
        Entry(fL,textvariable=self.e1,state="readonly").grid(row=2,column=1)
        Entry(fL,textvariable=self.e2).grid(row=3,column=1)
        Entry(fL,textvariable=self.e3,state="readonly").grid(row=4,column=1)
        self.b=Button(fL,text="Process Data",state=DISABLED,command=self.PDclicked)
        self.b.grid(row=5,column=0,columnspan=2,sticky=EW)

        Label(fR,text="Employees Per Department:").grid(row=0,column=0,columnspan=2)
        Label(fR,text="Environment").grid(row=1,column=0)
        Label(fR,text="Education").grid(row=2,column=0)                                                    
        Label(fR,text="Human Resources").grid(row=3,column=0)        
        Label(fR,text="Public Works").grid(row=4,column=0)        
        Label(fR,text="Transportation").grid(row=5,column=0)
        Label(fR,text="Total").grid(row=6,column=0)
        self.labelList=[]
        for i in range(1,7):
            l=Label(fR,text="-")
            l.grid(row=i,column=1)
            self.labelList.append(l)
            

    def loadCSVclicked(self):
        self.fileName=filedialog.askopenfilename()
        self.csvData = self.loadCSVfile() 
        if self.csvData == None:
            messagebox.showerror("ERROR", "CSV file invalid!")
            self.e1.set(" ")
            return None
        self.e1.set(self.fileName)
        self.b["state"]="active"

 

    def loadCSVfile(self):
        try:
            self.f=open(self.fileName,"r")
            self.r=csv.reader(self.f)
            self.csvList=[]
            for row in self.r:
                self.csvList.append(row)
            return self.csvList[1:]
        except:
            return None

    def PDclicked(self):
        try:
            self.htmlData=self.downloadData(self.e2.get())
        except:
            messagebox.showerror("ERROR", "URL or Data invalid!")
            return None
        self.convertedCSVdata=self.convertHTMLtoCSVFormat(self.htmlData)
        self.a = self.mergeData(self.convertedCSVdata,self.csvData)
        self.saveData(self.a)
        self.calculate()
        

        
    def downloadData(self,url):
        self.response = urllib.request.urlopen(url)
        self.data=self.response.read()
        self.text=str(self.data)
        self.HTMLdata=findall("<td>([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td>",self.text)
        return self.HTMLdata[1:]

    

    def convertHTMLtoCSVFormat(self,data):
        self.nameList=[]
        for item in data:
            self.nameList.append(item[0])
        self.new=[]
        for name in self.nameList:
            a = name.split(" ")
            self.new.append(a[::-1])
        for i in range(len(data)):
            self.new[i].append(data[i][2])
            self.new[i].append(data[i][1])
        return self.new


    def mergeData(self,htmlData,csvData):
        self.dict={}
        for info in csvData:
            self.dict[info[0]+","+info[1]]=info[2:][::-1]
        for info in htmlData:
            self.dict[info[0]+","+info[1]]=info[2:][::-1]
        for info in csvData:
            try:
                info[3]=int(info[3])
                indx=csvData.index(info)
                self.dict[csvData[indx][0]+","+csvData[indx][1]][0]=info[3]
            except:
                pass
        for key in list(self.dict.keys()):
            if self.dict[key][1]=="Parks and Recreation":
                self.dict[key][1]="Environment"
        return self.dict

    def saveData(self,adict):
        self.List=[]
        for key in list(adict.keys()):
            name=key.split(",")
            self.List.append([adict[key][1],name[0],name[1],adict[key][0]])
        self.List.sort()
        self.saveName=filedialog.asksaveasfilename()
        self.e3.set(self.saveName)
        self.newf=open(self.saveName,"w")
        self.w=csv.writer(self.newf)
        self.w.writerow(["Name","Salary","Department"])                            
        for line in self.List:
            info=[line[1]+","+line[2],line[3],line[0]]
            self.w.writerow(info)
        self.newf.close()

    def calculate(self):
        self.numEn=0
        self.numEd=0
        self.numHR=0
        self.numPW=0
        self.numT=0
        self.num=0
        for item in self.List:
            if item[0]=="Environment":
                self.numEn = self.numEn +1
            elif item[0]=="Education":
                self.numEd = self.numEd +1
            elif item[0]=="Human Resources":
                self.numHR = self.numHR +1
            elif item[0]=="Public Works":
                self.numPW = self.numPW +1
            elif item[0]=="Transportation":
                self.numT = self.numT +1
            self.num=self.num+1
        self.numList=[self.numEn,self.numEd,self.numHR,self.numPW,self.numT,self.num]
        for ind in range(len(self.numList)):
            self.labelList[ind]["text"]=str(self.numList[ind])
            


w = Tk()
w.title("City of Shamalamadingdong")
app = mergeData(w)
w.mainloop()

            
