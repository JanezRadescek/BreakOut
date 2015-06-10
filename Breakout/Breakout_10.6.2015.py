from tkinter import *
from random import randint
import math
import winsound

RADIJ_KROGLE = 5
SPEED_PLO = 5
SPEED_KRO = 5
CANVAS_H = 600
CANVAS_W = 600
SPEED_UPDATE = 20
LIFE = 3
ZIDAK_VIS = 10
ZIDAK_DOL = 20
PLOSCEK_VIS = 5
PLOSCEK_DOL = 50


root = Tk()


class Krogla:
    def __init__(self, master):
        self.life = LIFE
        self.x = 300
        self.y = 500
        self.speed = SPEED_KRO
        self.smer = -randint(50, 130)
        self.krogla = master.create_oval(self.x-RADIJ_KROGLE, self.y-RADIJ_KROGLE,
                                         self.x+RADIJ_KROGLE, self.y+RADIJ_KROGLE, fill="red")
        self.master = master

    def premik(self, plo_x):
        premik_x = self.speed*math.cos(math.pi*self.smer/180)
        premik_y = self.speed*math.sin(math.pi*self.smer/180)
        self.x += premik_x
        self.y += premik_y
        self.master.coords(self.krogla, self.x-RADIJ_KROGLE, self.y-RADIJ_KROGLE,
                           self.x+RADIJ_KROGLE, self.y+RADIJ_KROGLE)
        self.odboj()
        self.odboj_plo(plo_x)

    def odboj(self):

        if self.x <= RADIJ_KROGLE or self.x >= CANVAS_W - RADIJ_KROGLE:
            self.smer = 180-self.smer

        if self.y <= 0:
            self.smer = -self.smer

        if self.y >= CANVAS_H:
            self.life -= 1
            self.x = 300
            self.y = 500
            self.smer = randint(0, 360)
            if self.life == 0:
                print("THE END")
                self.x = 300
                self.y = 500
                self.speed = 0

    def odboj_plo(self, plo_x):
        if self.y >= 580 - (RADIJ_KROGLE + PLOSCEK_VIS) and self.x <= plo_x + 50 and self.x >= plo_x - 50:
            self.smer = -self.smer
            self.smer += (self.x - plo_x)/1.5


class Plošček:
    def __init__(self, master):
        self.x = 300
        self.y = 580
        self.hitrost = SPEED_PLO
        self.master = master
        self.plošček = self.master.create_rectangle(self.x-PLOSCEK_DOL,self.y-PLOSCEK_VIS,self.x+PLOSCEK_DOL,
                                                    self.y+PLOSCEK_VIS, fill="green")
        self.master.bind("<Motion>", self.prestavi)


    def premik(self):
        self.master.bind("<Motion>", self.prestavi)

    def prestavi(self, event):
        if event.x > PLOSCEK_DOL and event.x < CANVAS_W - PLOSCEK_DOL:
            self.x = event.x
            self.master.coords(self.plošček, self.x-50, self.y-5, self.x+50, self.y+5)



class Zidak:

    def __init__(self, master, x, y):
        self.višina = ZIDAK_VIS
        self.dolžina = ZIDAK_DOL
        self.x = x
        self.y = y
        self.raz = 0
        self.zidak = master.create_rectangle(self.x - self.dolžina, self.y - self.višina,
                                             self.x + self.dolžina, self.y + self.višina, fill="yellow")
        self.master = master

    def zbrisi(self, kro_x, kro_y):
        self.raz = math.sqrt((self.x - kro_x)**2 + (self.y - kro_y)**2)
        if self.raz <= RADIJ_KROGLE + self.dolžina:

            if kro_y <= self.y + self.višina and kro_y >= self.y - self.višina:
                aplikacija.krogla.smer = 180 - aplikacija.krogla.smer
            else:
                aplikacija.krogla.smer = -aplikacija.krogla.smer

            self.master.delete(self.zidak)
            return True
        return False


class Breakout:

    def __init__(self, master):
        self.canvas = Canvas(master, width=CANVAS_W, height=CANVAS_H, bg="white")
        self.img = PhotoImage(file="bga.png")
        self.canvas.create_image(0,0, anchor=NW, image = self.img)

        self.difficulty = 0

        winsound.PlaySound("XXYYZZ.wav", winsound.SND_ASYNC|winsound.SND_LOOP)

        self.canvas.grid(row=0, column=1)
        self.krogla = Krogla(self.canvas)
        self.plošček = Plošček(self.canvas)

        self.read()

        self.zidaki = []
        for a in range(9):
            for b in range(self.difficulty):
                self.zidaki.append(Zidak(self.canvas, 50 + a*60, 50 + b*40))

    def premakni(self):
        self.krogla.premik(self.plošček.x)
        for i, zidak in enumerate(self.zidaki):
            if zidak.zbrisi(self.krogla.x, self.krogla.y):
                del self.zidaki[i]
                break

        self.canvas.after(SPEED_UPDATE, self.premakni)

    def read(self):
        with open("ime.txt") as f:
            for vrstica in f:
                self.difficulty = int(vrstica)



aplikacija = Breakout(root)
aplikacija.premakni()
root.mainloop()
