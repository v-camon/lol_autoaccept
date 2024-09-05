from lcuapi import LCU, Event, EventProcessor
import time
import tkinter as tk
from PIL import Image, ImageTk
import threading
import pythoncom
import sys


       




def btnmain():
        lobby.searchState()
        lobby.isLeader()

        search.start()

        
        graf.imgstate(2)
        search.readyCheck()





class interface:
    def __init__(self):
        self.run = False
        self.main_thread = None

    def main(self):
        self.Graf = tk.Tk()
        self.Graf.title("AC")
        self.Graf.configure(bg="#373737")
        self.canvas = tk.Canvas(self.Graf, width=37, height=37, bg='#373737', highlightthickness=0)
        self.Graf.resizable(False, False)
        icon = Image.open(r".\data\logo.ico")
        icon = ImageTk.PhotoImage(icon)
        self.Graf.iconphoto(True, icon)
        self.Graf.wm_iconbitmap(r".\data\logo.ico")
        bold_font = ("Arial", 9, "italic", "bold")
        self.button = tk.Button(text='START', font=bold_font, command=self.btnstart, bg="#8D8D8D", height=1, width=7, state=tk.DISABLED)
        self.button.place(relx=0.57, rely=0.5, anchor="center")
        graf.imgstate(0)
        self.Graf.protocol("WM_DELETE_WINDOW", on_closing)
        self.Graf.mainloop()
        
        

    def imgstate(self,state):
        global current_state
        rutas = [r".\data\state_notReady.png",
                r".\data\state_ready.png",
                r".\data\state_search.png",
                r".\data\state_check.png"]
        if current_state!=state:
            current_state = state
            canvas = tk.Canvas(self.Graf, width=37, height=37, bg='#373737', highlightthickness=0)
            canvas.place(relx=0.3, rely=0.5, anchor="center")
            setimg = Image.open(rutas[state])
            setimg = setimg.resize((37,37))
            self.img = ImageTk.PhotoImage(setimg)
            canvas.delete("all")
            canvas.create_image(0, 0, anchor="nw", image=self.img)
        else:
            pass
        
    
    def btnstart(self):
        if self.run:
            self.run = False
            self.button.config(bg="#00B960", text="START")
            if self.main_thread:
                search.stop()
                self.main_thread = None
        
        else:
            self.run = True
            self.button.config(bg="#B90000", text="STOP")
            self.main_thread = threading.Thread(target=btnmain)
            self.main_thread.start()



def on_closing():
    print("Exiting")
    graf.Graf.quit()
    sys.exit()


class Search:    
    def start(self):
        if not lobby.isSearching and lobby.leader:
            lcu.post('/lol-lobby/v2/lobby/matchmaking/search')
        self.running = True
               

    def stop(self):
        lcu.delete('/lol-lobby/v2/lobby/matchmaking/search')
        print('stop Search')
        self.running = False
        graf.imgstate(1)

    def readyCheck(self):
        while self.running:
            print ('Not match yet')
            phase = lcu.get('/lol-gameflow/v1/gameflow-phase')
            print(phase)
            if phase == 'ReadyCheck':
                self.accept()
                break
            graf.imgstate(2)
            time.sleep(2)

    def accept(self):
        lcu.post('/lol-matchmaking/v1/ready-check/accept')
        print('Accepted')
        self.checkDodge()


    def checkDodge(self):
        graf.imgstate(3)
        while True:
            phase = lcu.get('/lol-gameflow/v1/gameflow-phase')
            print(phase)

            if phase == 'Matchmaking' or phase == 'Lobby' or phase == "ReadyCheck":
                print ('Repeat')
                self.readyCheck()
                break
            

            if phase == 'InProgress': 
                print('exiting')
                graf.Graf.quit()
                exit()
            
            time.sleep(5)





class Lobby:
    def searchState(self):
        state =  lcu.get('/lol-gameflow/v1/gameflow-phase')
        print(state)
        if state == 'Matchmaking':
            self.isSearching = True
            return
        self.isSearching = False
    
    def isLeader(self):
        self.leader = lcu.get('/lol-lobby/v2/lobby')
        self.leader = self.leader['localMember']['isLeader']
        print(self.leader)









lcu = LCU()

def wait_for_client_to_open():
    pythoncom.CoInitialize()
    lcu.wait_for_client_to_open()
    graf.imgstate(1)
    graf.button.config(bg="#00B960",state=tk.NORMAL)
    time.sleep(1)
    


threading.Thread(target=wait_for_client_to_open).start()



current_state = 73
search = Search()
lobby = Lobby()
graf = interface()
graf.main()
