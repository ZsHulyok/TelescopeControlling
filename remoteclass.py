import matplotlib
matplotlib.use('Agg')

import tkinter
import sys
from tkinter import *
from threading import *
from time import sleep
import RPi.GPIO as GPIO
import queue
from multiprocessing import Queue, Process
import math
import smbus
from tkinter import scrolledtext, Text
#_________Motor1-hez tartozó gpio portok
DIR = 20
STEP = 16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
Motor1_M0 = 23
Motor1_M1 = 24
GPIO.setup(Motor1_M0, GPIO.OUT)
GPIO.setup(Motor1_M1, GPIO.OUT)
sebesség = 1
delay = 0.00208

forgás = None
#__________giroszkóp
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
bus = smbus.SMBus(1) 
address = 0x68  
bus.write_byte_data(address, power_mgmt_1, 0)
#_________Menüsor

class MenuBar(tkinter.Menu):
    def __init__(self, parent):
        tkinter.Menu.__init__(self, parent)

        fileMenu = tkinter.Menu(self, tearoff=False)
        helpMenu = tkinter.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=fileMenu)
        fileMenu.add_command(label="Beállítások", underline=1, command = self.Beállítások)
        fileMenu.add_command(label="Exit", underline=1, )
        self.add_cascade(label="Help", underline=0, menu=helpMenu)
        helpMenu.add_command(label="Készítők", underline=1)
    
#____________________________Moto1r lépésfelbontás definíciói
    def Fél(self):
        
        GPIO.output(Motor1_M0, GPIO.HIGH)
        GPIO.output(Motor1_M1, GPIO.LOW)
    
    def Egész(self):
        
        GPIO.output(Motor1_M0, GPIO.LOW)
        GPIO.output(Motor1_M1, GPIO.LOW)
        
    def Nyolcad(self):
        
        GPIO.output(Motor1_M0, GPIO.LOW)
        GPIO.output(Motor1_M1, GPIO.HIGH)
        
    def Tizenhatod(self):
        
        GPIO.output(Motor1_M0, GPIO.HIGH)
        GPIO.output(Motor1_M1, GPIO.HIGH)
#________________Beállítások menü        
    def Beállítások(self):
        Beállítás_ablak = Tk()
        Beállítás_ablak.title("Beállítások")
        Beállítás_ablak.geometry("400x240+300+300")
        v = IntVar()
        v1 = IntVar()
    
        Motor1_sebesség = DoubleVar()
        Motor2_sebesség = DoubleVar()
#_______Motor1 beállításai________
        self.Motor1_Beállítás_Cimke = Label(Beállítás_ablak, text = "Motor1 Lépésfelbontás")
        self.Motor1_Beállítás_Cimke.grid(row = 0, sticky = W, pady = 10)
        self.Fél_lépés_Motor1 = Radiobutton(Beállítás_ablak, text="Fél", variable=v, value = 1, command = self.Fél)
        self.Fél_lépés_Motor1.grid(row = 1, sticky = W, padx = 30)
        self.Egész_lépés_Motor1 = Radiobutton(Beállítás_ablak, text="Egész", variable=v, value = 2, command = self.Egész )
        self.Egész_lépés_Motor1.grid(row = 2,sticky = W, padx = 30)
        self.Nyolcad_lépés_Motor1 = Radiobutton(Beállítás_ablak, text="Nyolcad", variable=v, value = 3, command = self.Nyolcad)
        self.Nyolcad_lépés_Motor1.grid(row = 3,sticky = W, padx = 30)
        self.Tizenhatod_lépés_Motor1 = Radiobutton(Beállítás_ablak, text="Tizenhatod", variable=v, value = 4, command = self.Tizenhatod )
        self.Tizenhatod_lépés_Motor1.grid(row = 4,sticky = W, padx = 30)
        self.Motor1_sebesség_cimke = Label(Beállítás_ablak, text = "Motor1 sebesség")
        self.Motor1_sebesség_cimke.grid(row = 5, sticky = W, pady = 10)
        self.Motor1_sebesség = Scale(Beállítás_ablak, from_ = 1, to = 100, variable = Motor1_sebesség, orient = HORIZONTAL)
        self.Motor1_sebesség.grid(row = 6, sticky = W, padx = 30)
    
#________Motor2 beállításai_________
        self.Motor2_Beállítás_Cimke = Label(Beállítás_ablak, text = "Motor2 Lépésfelbontás")
        self.Motor2_Beállítás_Cimke.grid(row = 0, column = 1, sticky = W, padx = 50, pady = 10)
        self.Fél_lépés_Motor2 = Radiobutton(Beállítás_ablak, text="Fél", variable=v1, value = 1, command = self.Fél)
        self.Fél_lépés_Motor2.grid(row = 1, column = 1, sticky = W, padx = 80)
        self.Egész_lépés_Motor2 = Radiobutton(Beállítás_ablak, text="Egész", variable=v1, value = 2, command = self.Egész )
        self.Egész_lépés_Motor2.grid(row = 2, column = 1, sticky = W, padx = 80)
        self.Nyolcad_lépés_Motor2 = Radiobutton(Beállítás_ablak, text="Nyolcad", variable=v1, value = 3, command = self.Nyolcad)
        self.Nyolcad_lépés_Motor2.grid(row = 3, column = 1, sticky = W, padx = 80)
        self.Tizenhatod_lépés_Motor2 = Radiobutton(Beállítás_ablak, text="Tizenhatod", variable=v1, value = 4, command = self.Tizenhatod )
        self.Tizenhatod_lépés_Motor2.grid(row = 4, column = 1, sticky = W, padx = 80)
        self.Motor2_sebesség_cimke = Label(Beállítás_ablak, text = "Motor1 sebesség")
        self.Motor2_sebesség_cimke.grid(row = 5, column = 1, sticky = W, padx = 50, pady = 10)
        self.Motor2_sebesség = Scale(Beállítás_ablak, from_ = 1, to = 100, variable = Motor2_sebesség, orient = HORIZONTAL)
        self.Motor2_sebesség.grid(row = 6, column = 1, sticky = W, padx = 80)
        self.Gomb_Kész = Button(Beállítás_ablak, text = "Kész", )
        self.Gomb_Kész.grid(row = 7, columnspan = 2)
        self.Beállítás_ablak.mainloop()
             

  
    
#___________________________Főablak
class Ablak(tkinter.Tk):
    def __init__(self,q):
        tkinter.Tk.__init__(self, )
        self.queue = q
        menubar = MenuBar(self)
        self.config(menu=menubar)
#_______________Fejlécek,cimkék        
        
        self.cimke1 = Label(self, text="ALT kordináta megadása", bg = "LightCyan2")
        self.cimke1.grid(columnspan = 2, sticky = E+W+S+N, pady =10)
        
        self.fok_X_cimke = Label(self, text="Fok")
        self.fok_X_cimke.grid(row =1, sticky = E)
        
        self.perc_X_cimke = Label(self, text="Perc")
        self.perc_X_cimke.grid(row =2, sticky = E )
        
        self.másodperc_X_cimke = Label(self, text="Másodperc")
        self.másodperc_X_cimke.grid(row = 3, sticky = E)

        self.cimke3 = Label(self, text="AZ kordináta megadása", bg = "LightCyan2")
        self.cimke3.grid(row = 4, columnspan = 2, sticky = E+W+S+N, pady = 10)
        
        self.fok_Y_cimke = Label(self, text="Fok")
        self.fok_Y_cimke.grid(row = 5, sticky = E)
        
        self.perc_Y_cimke = Label(self, text="Perc")
        self.perc_Y_cimke.grid(row =6, sticky = E)
        
        self.másodperc_Y_cimke= Label(self, text="Másodperc")
        self.másodperc_Y_cimke.grid(row =7, sticky = E)

        self.automata_vezérlés_cimke=Label(self, text="Automata vezérlés", bg = "navajo white")
        self.automata_vezérlés_cimke.grid(row =8, columnspan = 2, sticky = N+W+E+S, pady =10)
        
        self.kézi_vezérlés_cimke=Label(self, text="Kézi vezérlés", bg = "navajo white")
        self.kézi_vezérlés_cimke.grid(row =13, columnspan = 2, sticky = N+W+E+S, pady =10)
#______________Beviteli mezők_________________________________________
        self.fok_X_mező = Entry(self, width = 3)
        self.fok_X_mező.grid(row =1, column=1, sticky = W)
        
        self.perc_X_mező = Entry(self, width = 3)
        self.perc_X_mező.grid(row =2, column=1, sticky = W)
        
        self.másodperc_X_mező = Entry(self, width = 3)
        self.másodperc_X_mező.grid(row = 3, column = 1, sticky = W)
        
        self.fok_Y_mező = Entry(self, width = 3)
        self.fok_Y_mező.grid(row =5, column =1, sticky = W)
        
        self.perc_Y_mező = Entry(self, width = 3)
        self.perc_Y_mező.grid(row=6,column=1, sticky = W )
        
        self.másodperc_Y_mező = Entry(self, width = 3)
        self.másodperc_Y_mező.grid(row =7, column =1, sticky = W )

#______________Vezérlő gombok________________________________________
        self.Start_gomb = Button(self, text="Start", command = self.Automata_beállítás)
        self.Start_gomb.grid(row = 9, columnspan = 2, sticky = E+W+S+N)

        """self.Stop_gomb = Button(self, text="Stop", command = self.Megszakítás)
        self.Stop_gomb.grid(row = 10, columnspan = 2, sticky = E+W+S+N)"""

        self.Törlés_gomb = Button(self, text="Törlés")
        self.Törlés_gomb.grid(row = 11, columnspan = 2, sticky = E+W+S+N)

        self.Kilépés_gomb = Button(self, text="Kilépés", command = self.Kilépés)
        self.Kilépés_gomb.grid(row = 12,columnspan = 2, sticky = E+W+S+N)

        self.Fel_gomb = Button(self, text="Fel")
        self.Fel_gomb.grid(row = 14, columnspan = 2, sticky = E+W+S+N)

        self.Bal_gomb = Button(self, text="Bal")
        self.Bal_gomb.grid(row = 15, sticky = E+W+S+N)

        self.Jobb_gomb = Button(self, text="Jobb")
        self.Jobb_gomb.grid(row = 15, column =1,sticky = E+W+S+N)

        self.Le_gomb = Button(self, text="Le")
        self.Le_gomb.grid(row = 16,columnspan = 2, sticky = E+W+S+N)
#______________Gombokhoz tartozó Event Handler______________________
        self.Fel_gomb.bind("<ButtonPress-1>", lambda event : self.Fel())
        self.Fel_gomb.bind("<ButtonRelease-1>",lambda event :self.Break())

        self.Le_gomb.bind("<ButtonPress-1>", lambda event : self.Le())
        self.Le_gomb.bind("<ButtonRelease-1>",lambda event :self.Break())

        self.Bal_gomb.bind("<ButtonPress-1>", lambda event : self.Bal())
        self.Bal_gomb.bind("<ButtonRelease-1>",lambda event :self.Break())

        self.Jobb_gomb.bind("<ButtonPress-1>", lambda event : self.Jobb())
        self.Jobb_gomb.bind("<ButtonRelease-1>",lambda event :self.Break())
#_______________________Text box____________________________________________
        
        self.txt_box = scrolledtext.ScrolledText(self)  
        self.txt_box.grid(row=0, column=2, columnspan = 6, rowspan=15, sticky = W)
#______________________Giroszkóp pozíció_________________________
        self.giroszkóp_pozíció_cimke = Label(self, text="Giroszkóp pozíciója", bg = "LightCyan2")
        self.giroszkóp_pozíció_cimke.grid(row = 14, column = 2, columnspan = 4, sticky = S, pady = 10)
        
        self.giroszkóp_x_pozíció_cimke = Label(self, text = "X pozíció:")
        self.giroszkóp_x_pozíció_cimke.grid(row = 15, column = 2)
        
        self.x_giroszkóp_pozíció = Entry(self)
        self.x_giroszkóp_pozíció.grid(row = 15, column = 3)

        self.giroszkóp_y_pozíció_cimke = Label(self, text = "Y pozíció:")
        self.giroszkóp_y_pozíció_cimke.grid(row = 15, column = 4)
        
        self.y_giroszkóp_pozíció = Entry(self)
        self.y_giroszkóp_pozíció.grid(row = 15, column = 5)
        
        self.giroszkóp_pozíció_cimke = Label(self, text="Cél pozíciója", bg = "LightCyan2")
        self.giroszkóp_pozíció_cimke.grid(row = 16, column = 2, columnspan = 4, sticky = S, pady = 10)
        
        self.cél_x_pozíció_cimke = Label(self, text = "X pozíció:")
        self.cél_x_pozíció_cimke.grid(row = 17, column = 2)
        
        self.x_cél_decimális = Entry(self)
        self.x_cél_decimális.grid(row = 17, column = 3)

        self.cél_x_pozíció_cimke = Label(self, text = "Y pozíció:")
        self.cél_x_pozíció_cimke.grid(row = 17, column = 4)
        
        self.y_cél_decimális = Entry(self)
        self.y_cél_decimális.grid(row = 17, column = 5)
        
#________________Léptetőmotorok vezérlése  
    def motor2(self):
        pass   

    def motor1(self, forgásirány):
        
        GPIO.output(DIR, forgásirány)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        

#____________Giroszkóp       
    def giroszkóp(self, queue):
        
        while True:
            sleep(0.1)

            accel_xout = self.read_word_2c(0x3b)
            accel_yout = self.read_word_2c(0x3d)
            accel_zout = self.read_word_2c(0x3f)

            accel_xout_scaled = accel_xout / 16384.0
            accel_yout_scaled = accel_yout / 16384.0
            accel_zout_scaled = accel_zout / 16384.0



            #print ("x rotation: " , self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
            xelfordulás = self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
            yelfordulás = self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
            queue.put(yelfordulás)
            queue.put(xelfordulás)
            print ("y rotation: " , self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
            print ("X rotation: " , self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
            sleep(0.5)
            
    def read_word(self,adr):
        high = bus.read_byte_data(address, adr)
        low = bus.read_byte_data(address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a,b):
        return math.sqrt((a*a)+(b*b))


    def get_y_rotation(self, x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self, x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)     
            
        pass
    def Automata_beállítás(self):
        self.Start_gomb.config(state=DISABLED)
        self.txt_box.insert('end',"a távcső beállítása folyamatban\n")
        self.folyamat1 = Process(target=self.giroszkóp, args=(self.queue,))
        self.folyamat1.start()
        self.after(600, self.Ellenőrzés)
#___________Vezérlőgombok definíciói      
        
    """def Megszakítás(self):
        os.system('pkill ',self.folyamat1)"""

    """def Törlés(self):
        pass"""

    def Kilépés(self):
        GPIO.cleanup()

    def Le(self):
        global forgás
        forgás = self.after(0, self.Le)
        self.motor1(0) #...0 = forgásirány óramutató járásával megeggyező
        pass
    def Fel(self):
        
        global forgás
        forgás = self.after(0, self.Fel)
        self.motor1(1) #...1 = forgásirány óramutató járásával ellenkező
        
        pass
    def Bal(self):
        global forgás
        forgás = self.after(80, self.Bal)
        self.txt_box.insert('end', "A Bal gomb lenyomva\n")
        self.txt_box.configure(foreground='green')
        pass
    def Jobb(self):
        global forgás
        forgás = self.after(80, self.Jobb)
        self.txt_box.insert('end', "A Jobb gomb lenyomva\n")
        self.txt_box.configure(foreground='green')
        pass
    def Break(self):
        global forgás
        self.after_cancel(forgás)
        self.txt_box.insert('end', "A gomb felengedve\n")
        self.txt_box.configure(foreground='red')
        
        pass
#___________Giroszkóp működésének ellenőrzése
    def Ellenőrzés(self):
        if (self.folyamat1.is_alive()):
            self.after(600, self.Ellenőrzés)
            self.x_giroszkóp_pozíció.delete(0, END)
            self.x_giroszkóp_pozíció.insert(0, self.queue.get(0))
            self.y_giroszkóp_pozíció.delete(0,END)
            self.y_giroszkóp_pozíció.insert(0, self.queue.get(0))
            return

        else:
            try:
                self.txt_box.insert('end', "Giroszkóp Hiba!\n")
                self.Start_gomb.config(state=NORMAL)
                
            except queue.Empty:
                self.txt_box.insert('end', "Nincs érték!\n")


def main():
    q = Queue()
    app = Ablak(q)
    app.title("Teleszkóp vezérlés")
    app.geometry("800x600+300+300")
    app.mainloop()  
    
if __name__ == "__main__":
    main()    
