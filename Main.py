import cv2 as c
from tkinter import *
from PIL import Image, ImageTk 
import os
import numpy as np
import face_recognition as fs


StudentList = set()
vid = c.VideoCapture(0)
# width, height = 800, 600
path = 'D:/collage/semister 1/TermPaper_DBMS/project/image'
images = []
classNames = []

myList = os.listdir(path)
# print(myList)

for cl in myList:
     curImg = c.imread(f'{path}/{cl}')
     images.append(curImg)
     classNames.append(os.path.splitext(cl)[0])

def open_camera(): 
     global StudentList
     _, img = vid.read() 
     # imgs = c.resize(img,(0,0),None,0.25,0.25)
     imgs = c.resize(img,(0,0),None,0.75,0.75)
     imgs = c.cvtColor(imgs, c.COLOR_BGR2RGB)
     facesCurFrame = fs.face_locations(imgs)
     encodeCurFrame= fs.face_encodings(imgs,facesCurFrame)

     for encodeFace, faceLoc in zip(encodeCurFrame,facesCurFrame):
          matches = fs.compare_faces(encodeListKnown,encodeFace)
          faceDis = fs.face_distance(encodeListKnown,encodeFace)
          # print(faceDis)
          matchIndex = np.argmin(faceDis)

          if matches[matchIndex]:
               name = classNames[matchIndex].upper()
               StudentList.add(name)
               StudentList = set(StudentList)
               string = ""
               if len(StudentList) != 0:
                    for stud in StudentList:
                         string = string +"\n" +stud
                    ListOfStudentWidget.config(text=string)
               # print(faceLoc)
               y1,x2,y2,x1 = faceLoc
               c.rectangle(imgs,(x1,y1),(x2,y2),(0,255,0),2)
               c.rectangle(imgs,(x1,y2-30),(x2,y2),(0,0,255),-1)
               c.putText(imgs,name,(x1,y2),c.FONT_HERSHEY_COMPLEX,0.01*(float(x2)-float(x1))*0.60,(255,255,255),2)
     captured_image = Image.fromarray(imgs)
     photo_image = ImageTk.PhotoImage(image=captured_image) 
     cameraView.photo_image = photo_image 	
     cameraView.configure(image=photo_image) 

     cameraView.after(1, open_camera)

def findEncodings(images):
     encodeList = []
     for img in images:
          img= c.cvtColor(img,c.COLOR_BGR2RGB)
          encode= fs.face_encodings(img)[0]
          encodeList.append(encode)
     print("Main work is complete")
     return encodeList

encodeListKnown = findEncodings(images)

# vid.set(c.CAP_PROP_FRAME_WIDTH, width) 
# vid.set(c.CAP_PROP_FRAME_HEIGHT, height) 


app = Tk() 

app.bind('<Escape>', lambda e: app.quit())
# frame component

frame = Frame(app,background="#040D12")
frame.pack(side="left",expand=True,fill="both")

Title = Label(frame,text="Attendance App",fg="#183D3D",background="#040D12")
Title.pack(side="top")

ListOfStudentWidget = Label(frame,text="list",background="#183D3D",fg="#93B1A6")
ListOfStudentWidget.pack(side="top",expand=True,fill="y")

# non-Frame component
cameraView = Label(app) 
cameraView.pack(side="right") 

button1 = Button(frame, text="Open Camera", command=open_camera,fg="#183D3D",bg="#93B1A6") 
button1.pack(side="bottom") 

# #040D12
# #183D3D
# #5C8374
# #93B1A6
app.mainloop() 
