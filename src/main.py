from tkinter import *
from PIL import Image
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

imageIndex = 0
classes = []
imageHovering = False
x, y = 0, 0

def setHovering(self):
    global imageHovering
    imageHovering = True

def setNotHovering(self):
    global imageHovering
    imageHovering = False

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
        radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.sharedVariable)
        radiobutton.grid(row=len(self.radiobuttons)+1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.radiobuttons.append(radiobutton)

    def get(self):
        return self.sharedVariable.get()
    def set(self, val):
        self.sharedVariable.set(val)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{1000}x{800}")
        self.title("FastYolo")

        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.classPicker = classPicker(self, "Classes", classes)
        self.classPicker.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="Add Class", command=self.addClassEvent)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
    
        self.classEntry = customtkinter.CTkEntry(self, placeholder_text="Class Name")
        self.classEntry.grid(row=2, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.imageData = customtkinter.CTkImage(light_image=Image.open("/Users/zhiyuan/Desktop/ThomasTheDankEngineCode/Python/ML/FastYolo/data/project1/rawImages/IMG_4874.JPG").resize((640, 640)).rotate(-90), size=(640, 640))
        self.mainImage = customtkinter.CTkLabel(self, image=self.imageData, text="")
        self.mainImage.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.mainImage.bind("<Enter>", setHovering)
        self.mainImage.bind("<Leave>", setNotHovering)

        # self.canvas = customtkinter.CTkCanvas(self, width=640, height=640, bg='#000000')
        # self.canvas.grid(row=0, column=2)

    def addClassEvent(self):
        className = self.classEntry.get()
        if className in classes or className=="":
            return
        
        classes.append(className)
        self.classPicker.addClass(className)


def getMouseLocation(e):
    x = e.x
    y = e.y
    print(x, y, imageHovering)

if __name__ == '__main__':
    app = App()
    app.bind("<Motion>", getMouseLocation)
    app.mainloop()