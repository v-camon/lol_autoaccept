from dataclasses import asdict
import tkinter as tk
import time
import pyautogui
from pynput.mouse import Button, Controller
from PIL import Image, ImageTk
import threading
import sys



mouse = Controller()






rutas_check = ['.\\data\\res_1.png',
               '.\\data\\res_2.png',
               '.\\data\\res_3.png'
               ]


a = 0
b = 1
c = 2
d = 3
x = 4
res1 = 0
res2 = 1
res3 = 2


global run
run = False







class img:
   
    def __init__(self,ruta):
        self.image = Image.open(ruta)


    def find(self):
        try:
            self.position = pyautogui.locateOnScreen(self.image)
        except pyautogui.ImageNotFoundException:
            self.position = None
    


class check_resolution:
    def __init__(self):
        self.ruta_base = None
        
        imagen_res1 = img(rutas_check[res1])
        imagen_res2 = img(rutas_check[res2])
        imagen_res3 = img(rutas_check[res3])

        imagen_res2.find()
        if imagen_res2.position:
            self.ruta_base = '.\\data\\res2\\'
            print('res2')
    
        imagen_res3.find()
        if imagen_res3.position:
            self.ruta_base = '.\\data\\res3\\'
            print('res3')
    
        imagen_res1.find()
        if imagen_res1.position:
            self.ruta_base = '.\\data\\res1\\'
            print('res1')


def create_images():
    global imagenA,imagenB,imagenC,imagenD,imagenX,check_res
    check_res=check_resolution()
    
    rutas = [check_res.ruta_base + 'a.png',
         check_res.ruta_base + 'b.png',
         check_res.ruta_base + 'c.png',
         check_res.ruta_base + 'd.png',
         check_res.ruta_base + 'x.png',
         ]
    imagenA = img(rutas[a])
    imagenB = img(rutas[b])
    imagenC = img(rutas[c])
    imagenD = img(rutas[d])
    imagenX = img(rutas[x])
    
   
    




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
    create_images()
    time.sleep(1)

    imagenD.find()
    imagenX.find()

    if imagenD.position is None and imagenX.position:
        x, y, width, height = imagenX.position
        x += 37
        poss.get()
        mouse.position = (x,y)
        mouse.press(Button.left)
        mouse.release(Button.left)
        poss.ret()
        print('Starting search')
    else:
        print('Just Searching')
    


def search():
    time.sleep(3)
    imagenA.find()
    if imagenA.position is None:
        print("No match yet.")
        return
    x, y, width, height = imagenA.position
    x += 37
    y += 37
    # poss.get()
    mouse.position = (x, y)
    mouse.press(Button.left)
    mouse.release(Button.left)
    print("Autoaccept completed.")
    # poss.ret()
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
    
    imagenB.find()
    imagenC.find()

    
    if imagenB.position is not None or imagenC.position is not None:
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



def on_closing():
    print("Exiting")
    sys.exit()


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






Graf.protocol("WM_DELETE_WINDOW", on_closing)

Graf.mainloop()

