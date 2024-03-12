from dataclasses import asdict
import tkinter as tk
import time
import pyautogui
from pynput.mouse import Button, Controller
from PIL import Image, ImageTk
import threading



x=1
y=2

mouse = Controller()



global run
run = False


class poss:
    
    def get():
        global x2, y2
        x2, y2 = pyautogui.position()
        return x2, y2

   
    def ret():
        mouse.position = (x2,y2)
        

def frst ():
    state.search()
    run = True
    time.sleep(1)
    ruta_imagen_referencia_c = '.\data\\c.png'
    ruta_imagen_referencia_x = '.\data\\x.png'
    
    imagen_referencia_c = Image.open(ruta_imagen_referencia_c)
    imagen_referencia_x = Image.open(ruta_imagen_referencia_x)
    
    position_x = pyautogui.locateOnScreen(imagen_referencia_x)
    position_c = pyautogui.locateOnScreen(imagen_referencia_c)
    
    if position_c is None and position_x:
        x, y, width, height = position_x
        x += 37
        poss.get()
        mouse.position = (x,y)
        mouse.press(Button.left)
        mouse.release(Button.left)
        poss.ret()
        print('Starting searchig')
    else:
        print('Just Searching')
    
    search()


def search():
    time.sleep(3)
    ruta_imagen_referencia = '.\data\\a.png'
    imagen_referencia = Image.open(ruta_imagen_referencia)
    position = pyautogui.locateOnScreen(imagen_referencia)
    if position is None:
        print("No match yet.")
        return
    x, y, width, height = position
    x += 37
    y += 37
    poss.get()
    mouse.position = (x, y)
    mouse.press(Button.left)
    mouse.release(Button.left)
    print("Autoaccept completed.")
    poss.ret()
    state.check()
    time.sleep(10)
    check()
    





def start():
    global run
    if run:
        run = False
        button.config(bg="#00B960", text="START")
        state.ready()
    else:
        run = True
        button.config(bg="#B90000", text="STOP")
        threading.Thread(target=combined).start()





def combined():
    frst()
    auto_accept_thread()

def auto_accept_thread():
    while run:
        search()
        





def check():
    
    ruta_imagen_referencia_b = '.\data\\b.png'
    ruta_imagen_referencia_c = '.\data\\c.png'
    
    imagen_referencia_b = Image.open(ruta_imagen_referencia_b)
    imagen_referencia_c = Image.open(ruta_imagen_referencia_c)
    
    position_b = pyautogui.locateOnScreen(imagen_referencia_b)
    position_c = pyautogui.locateOnScreen(imagen_referencia_c)
    
    if position_b is not None or position_c is not None:
        print("Restarting search.")
        state.search()
        search()
    else:
        print('Exiting')
        Graf.quit()
        exit()



class state:
    def __init__(self):
        self.canvas_width = 37
        self.canvas_height = 37
        self.canvas = tk.Canvas(Graf, width=self.canvas_width, height=self.canvas_height, bg='#373737', highlightthickness=0)
        self.canvas.place(relx=0.3, rely=0.5, anchor="center")

    def ready(self):
        img_ready = Image.open('.\data\state_ready.png')
        img_ready = img_ready.resize((self.canvas_width, self.canvas_height))
        self.img = ImageTk.PhotoImage(img_ready)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def search(self):
        img_ready = Image.open('.\data\state_search.png')
        img_ready = img_ready.resize((self.canvas_width, self.canvas_height))
        self.img = ImageTk.PhotoImage(img_ready)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def check(self):
        img_ready = Image.open('.\data\state_check.png')
        img_ready = img_ready.resize((self.canvas_width, self.canvas_height))
        self.img = ImageTk.PhotoImage(img_ready)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)



Graf = tk.Tk()
Graf.title("AC")
Graf.configure(bg="#373737")

global canvas_height
global canvas_width
canvas_width = 37
canvas_height = 37
global canvas
canvas = tk.Canvas(Graf, width=canvas_width, height=canvas_height, highlightthickness=0, bg='#373737')


icon = Image.open(".\data\\logo.ico")
icon = ImageTk.PhotoImage(icon)
Graf.iconphoto(True, icon)
Graf.wm_iconbitmap(".\data\\logo.ico")
bold_font = ("Arial", 9, "italic", "bold")
button = tk.Button(text='START',font=bold_font, command=start, bg="#00B960",height=1, width=7)
button.place(relx=0.57, rely=0.5, anchor="center")

state = state()
state.ready()

Graf.resizable(False,False)


Graf.mainloop()

