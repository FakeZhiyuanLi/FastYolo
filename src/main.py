from tkinter import *
from PIL import Image, ImageTk
from augment import aug
import customtkinter
import pybboxes
import imgaug as ia
import imgaug.augmenters as iaa
import yaml
import os

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

basePath = f'/Users/zhiyuan/Desktop/ThomasTheDankEngineCode/Python/ML/FastYolo/data/project1'

imageIndex = 0
classes = []
classIndexes = dict()
imageHovering = False
leftButtonDown = False
x, y = 0, 0
startX, startY = 0, 0
numImages = len(os.listdir(f'{basePath}/rawImages'))
rawImageLocations = os.listdir(f'{basePath}/rawImages')
boundingBoxes = [[] for x in range(numImages)]
currentBounds = boundingBoxes[imageIndex]
currentClass = "NaN"

def setHovering(self):
    global imageHovering
    imageHovering = True

def setNotHovering(self):
    global imageHovering
    imageHovering = False

def incrementImageIndex(self):
    global imageIndex
    imageIndex += 1
    if imageIndex >= numImages:
        imageIndex = 0

def decrementImageIndex(self):
    global imageIndex
    imageIndex = imageIndex-1;
    if imageIndex < 0:
        imageIndex = numImages-1

def mouseDownEvent(self):
    global leftButtonDown, startX, startY
    if not imageHovering:
        return
    
    if leftButtonDown:
        leftButtonDown = False
        currentBounds.append([currentClass, min(startX, x), min(startY, y), max(startX, x), max(startY, y)])
        canvas.create_rectangle(min(startX, x), min(startY, y), max(startX, x), max(startY, y), fill='', outline='lime', width=3)
        canvas.create_text(min(startX, x)-10, min(startY, y)-10, text=currentClass, fill='white')
    else:
        leftButtonDown = True
        startX = x
        startY = y


class classPicker(customtkinter.CTkScrollableFrame):
    def __init__ (self, parent, title, values):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.sharedVariable = customtkinter.StringVar()

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.sharedVariable)
            radiobutton.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    def addClass(self, value):
        radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.sharedVariable, command=self.setClass)
        radiobutton.grid(row=len(self.radiobuttons)+1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.radiobuttons.append(radiobutton)

    def setClass(self):
        global currentClass
        currentClass = self.sharedVariable.get()

    def get(self):
        return self.sharedVariable.get()
    def set(self, val):
        self.sharedVariable.set(val)

class App(customtkinter.CTk):
    def __init__(self):
        global canvas
        super().__init__()
        self.geometry(f"{1100}x{800}")
        self.title("FastYolo")

        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.classPicker = classPicker(self, "Classes", classes)
        self.classPicker.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="Add Class", command=self.addClassEvent)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
    
        self.classEntry = customtkinter.CTkEntry(self, placeholder_text="Class Name")
        self.classEntry.grid(row=2, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.imageData = ImageTk.PhotoImage(Image.open(f'{basePath}/rawImages/{rawImageLocations[imageIndex]}').resize((640, 640)).rotate(-90), size=(640, 640))
        canvas = customtkinter.CTkCanvas(self, bg="gray", width=640, height=640, bd=0, highlightthickness=0, relief='ridge')
        canvas.create_image(0, 0, anchor=NW, image=self.imageData)
        canvas.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        canvas.bind("<Enter>", setHovering)
        canvas.bind("<Leave>", setNotHovering)

        self.forwardArrow = customtkinter.CTkButton(self, text="→ Next Image", command=self.forwardEvent)
        self.forwardArrow.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

        self.backArrow = customtkinter.CTkButton(self, text="← Previous Image", command=self.backEvent)
        self.backArrow.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

        self.imageIndexLabel = customtkinter.CTkLabel(self, text=f'Image {imageIndex+1}/{numImages}')
        self.imageIndexLabel.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        canvas.bind("<Button-1>", mouseDownEvent)

        self.doneButton = customtkinter.CTkButton(self, text="Done", command=self.finishedEvent)
        self.doneButton.grid(row=3, column=3, padx=10, pady=10, sticky="ew")


    def addClassEvent(self):
        className = self.classEntry.get()
        if className in classes or className=="":
            return
        
        classIndexes[className] = len(classes)
        classes.append(className)
        self.classPicker.addClass(className)

    def backEvent(self):
        boundingBoxes[imageIndex] = currentBounds
        decrementImageIndex(self)
        self.updateImage()

    def forwardEvent(self):
        boundingBoxes[imageIndex] = currentBounds
        incrementImageIndex(self)
        self.updateImage()

    def updateImage(self):
        global currentBounds
        currentBounds = boundingBoxes[imageIndex]
        self.imageData = ImageTk.PhotoImage(Image.open(f'{basePath}/rawImages/{rawImageLocations[imageIndex]}').resize((640, 640)).rotate(-90), size=(640, 640))
        canvas.create_image(0, 0, anchor=NW, image=self.imageData)
        self.imageIndexLabel.configure(text=f'Image {imageIndex+1}/{numImages}')
        for box in currentBounds:
            canvas.create_rectangle(box[1], box[2], box[3], box[4], fill='', outline='lime', width=3)
            canvas.create_text(min(box[1], box[3])-10, min(box[2], box[4])-10, text=box[0], fill='white')
        # self.mainImage = customtkinter.CTkLabel(self, image=self.imageData, text="")
        # self.mainImage.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        # self.mainImage.bind("<Enter>", setHovering)
        # self.mainImage.bind("<Leave>", setNotHovering)

    def finishedEvent(self):
        yoloBoundingBoxes = []
        reducedImages = []
        for imageIdx, arr in enumerate(boundingBoxes):
            currConvert = []
            for boundingBox in arr:
                height = boundingBox[4]-boundingBox[2]
                width = boundingBox[3]-boundingBox[1]
                # print(width, height)
                # print(boundingBox[1:5])
                converted = list(pybboxes.convert_bbox(boundingBox[1:5], from_type="voc", to_type="yolo", image_size=(640, 640)))
                currConvert.append([classIndexes[boundingBox[0]], converted[0], converted[1], converted[2], converted[3]])
            yoloBoundingBoxes.append(currConvert)
        # print(yoloBoundingBoxes)
        for i, image in enumerate(rawImageLocations):
            reducedImage = Image.open(f'{basePath}/rawImages/{image}').resize((640, 640)).rotate(-90)
            reducedImage.save(f'/Users/zhiyuan/Desktop/ThomasTheDankEngineCode/Python/ML/FastYolo/data/project1/edited/raw/{image}')
            reducedImages.append(reducedImage)
            with open(f'/Users/zhiyuan/Desktop/ThomasTheDankEngineCode/Python/ML/FastYolo/data/project1/edited/raw/{image[:-4]}.txt', 'w') as f:
                for box in yoloBoundingBoxes[i]:
                    f.write(f'{box[0]} {box[1]} {box[2]} {box[3]} {box[4]} \n')
        aug(reducedImages, yoloBoundingBoxes, epochs=5)

def getMouseLocation(e):
    global x, y
    x = e.x
    y = e.y
    # print(x, y, imageHovering, currentBounds)

if __name__ == '__main__':
    app = App()
    app.bind("<Motion>", getMouseLocation)
    app.mainloop()