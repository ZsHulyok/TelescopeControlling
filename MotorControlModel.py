import RPi.GPIO as GPIO
from time import sleep
from tkinter import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class MotorControlModel:
    def __init__(self, lep_Port, forgas_Port, lepesFelbontasM0Port, lepesFelbontasM1Port):
        self.max_kesleltetes = 0.208
        self.leptetes_Port = lep_Port
        self.forgas_Port = forgas_Port
        self.lepesfelbontas_M0_PORT = lepesFelbontasM0Port
        self.lepesfelbontas_M1_PORT = lepesFelbontasM1Port
        self.sebesseg_Arany = 1
        self.motorMode = StringVar()
        self.motorMode.set("Teljes")
        GPIO.setup(self.forgas_Port, GPIO.OUT)
        GPIO.setup(self.leptetes_Port, GPIO.OUT)
        GPIO.setup(self.lepesfelbontas_M0_PORT, GPIO.OUT)
        GPIO.setup(self.lepesfelbontas_M1_PORT, GPIO.OUT)

    def GetSebesseg(self):
        return float(self.max_kesleltetes / (float(self.sebesseg_Arany)))

    def MakeStep(self, forgasirany):
        GPIO.output(self.forgas_Port, forgasirany)
        GPIO.output(self.leptetes_Port, GPIO.HIGH)
        sleep(self.GetSebesseg())
        GPIO.output(self.leptetes_Port, GPIO.LOW)
        sleep(self.GetSebesseg())

    def SetSpeed(self, value):
        self.sebesseg_Arany = value

    def SetMotorMode(self):
        if self.motorMode.get() == "Teljes":
            GPIO.output(self.lepesfelbontas_M0_PORT, GPIO.LOW)
            GPIO.output(self.lepesfelbontas_M1_PORT, GPIO.LOW)
        if self.motorMode.get() == "Fel":
            GPIO.output(self.lepesfelbontas_M0_PORT, GPIO.HIGH)
            GPIO.output(self.lepesfelbontas_M1_PORT, GPIO.LOW)
        if self.motorMode.get() == "Nyolcad":
            GPIO.output(self.lepesfelbontas_M0_PORT, GPIO.LOW)
            GPIO.output(self.lepesfelbontas_M1_PORT, GPIO.HIGH)
        if self.motorMode.get() == "Tizenhatod":
            GPIO.output(self.lepesfelbontas_M0_PORT, GPIO.HIGH)
            GPIO.output(self.lepesfelbontas_M1_PORT, GPIO.HIGH)

    def SetTeljesMotorMode(self):
        GPIO.output(self.lepesfelbontas_M0_PORT, GPIO.LOW)
        GPIO.output(self.lepesfelbontas_M1_PORT, GPIO.LOW)

    def SetFelMotorMode(self):
        GPIO.output(self.lepesfelbontas_M0_PORT, GPIO.HIGH)
        GPIO.output(self.lepesfelbontas_M1_PORT, GPIO.LOW)

    def SetNyolcadMotorMode(self):
        GPIO.output(self.lepesfelbontas_M0_PORT, GPIO.LOW)
        GPIO.output(self.lepesfelbontas_M1_PORT, GPIO.HIGH)

    def SetTizenhatodMotorMode(self):
        GPIO.output(self.lepesfelbontas_M0_PORT, GPIO.HIGH)
        GPIO.output(self.lepesfelbontas_M1_PORT, GPIO.HIGH)
