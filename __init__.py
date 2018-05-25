
from Navegacion import mapa as m
from Navegacion import brujula as b
import pelotas as p
from tkinter import *
import tkinter.messagebox
import tkinter
import time
import serial

def mandar():
    global misi
    global misio
    compa=''
    compara=''
    ardu=True
    try:
        ser = serial.Serial(
            port='COM4',
            baudrate= 250000
            )
    except serial.SerialException:
        ardu=False
        msgeme("!Arduino no encontrado!")



    if ardu == True:
        ser.write('')
        time.sleep(1)
        ser.write('d')
        time.sleep(1)
        for i in misio:
            #ser.write(str(i))
            #ser.write(',')
            compa=compa+str(i)+','
            #time.sleep(1)
        #compa=compa+str(i)+'f'
        ser.write(compa)
        time.sleep(1)
        ser.write('f')
        time.sleep(1)
        t=ser.inWaiting()
        compara=ser.read(t)
        print (compara)
        ##print compa
        if compa == compara :
            selec="Transferencia correcta"
            num.config(text = selec, bg = "white")
        else:
           selec= "Transferencia incorrecta"
           num.config(text = selec, bg = "white")
        ser.close()
        del misi[:]
        del misio[:]
        misio=[' ']

def cali():
    compara=''
    ardu=True
    try:
        ser = serial.Serial(
            port='COM4',
            baudrate= 250000
            )
    except serial.SerialException:
        ardu=False
        msgeme("!Arduino no encontrado!")



    if ardu == True:
        ser.write('')
        time.sleep(1)
        ser.write('c')
        time.sleep(1)
        t=ser.inWaiting()
        compara=ser.read(t)
        print (compara)
        if 'c' == compara :
            selec="Iniciando calibracion"
            num.config(text = selec, bg = "white")
        else:
           selec= "Transferencia incorrecta"
           num.config(text = selec, bg = "white")
        ser.close()

def ini():
    compara=''
    ardu=True
    try:
        ser = serial.Serial(
            port='COM4',
            baudrate= 250000
            )
    except serial.SerialException:
        ardu=False
        msgeme("!Arduino no encontrado!")



    if ardu == True:
        ser.write('')
        time.sleep(1)
        ser.write('i')
        time.sleep(1)
        t=ser.inWaiting()
        compara=ser.read(t)
        print (compara)
        if 'i' == compara :
            selec="Iniciando mision"
            num.config(text = selec, bg = "white")
        elif 'I' == compara :
           selec= "No calibrado"
           num.config(text = selec, bg = "white")
        else :
           selec= "Transferencia incorrecta"
           num.config(text = selec, bg = "white")
        ser.close()



def generar_mapa():
    global mi_mapa
    for i in cruces:
        mi_mapa.definir_nodo(i)
    for i in adj:
        mi_mapa.agregar_distancia(i[0],i[1], i[2])

def msgeme(msg):
    eme = Toplevel()
    eme.title("Mensaje")
    var = StringVar()
    mensaje= Label(eme ,textvariable= var)
    var.set(msg)
    eme.iconbitmap('bunny.ico')
    mensaje.pack()
    eme.mainloop()

def sel():
    global mis_pelotas
    ppelotas={}
    np= 0
    for i in CheckVar:
        if CheckVar[i].get() == 1:
            ppelotas[np] = i
            mis_pelotas[np] = p.pelota(adj[i][0], adj[i][1])
            np = np + 1
    selection = " Numero de pelotas = \n" + str(np)
    if np > 0:
            selection = selection + "\n Posicion :\n" + str(ppelotas)
    else:
        selection = selection + "\n Posicion :\n"
    num.config(text = selection, bg = "white")
    if np >= 4:
        msgeme("!!Haz seleccionado mas de 3 pelotas!!")
    lp=len(mis_pelotas)
    if np == 0:
        if lp >= 1:
            for i in range(0,lp):
                del mis_pelotas[i]


def generar_camino():
    global mis_pelotas
    global misi
    global misio
    misi=[' ']
    misio=[]
    generar_mapa()
    origen = 'in'
    for i in mis_pelotas:
        distancia_1 = mi_mapa.distancia_entre('ho', mis_pelotas[i].consultar_posicion(1))
        generar_mapa()
        distancia_2 = mi_mapa.distancia_entre('ho', mis_pelotas[i].consultar_posicion(2))
        if distancia_1 <= distancia_2:
            mis_pelotas[i].establecer_distancia(distancia_1)
        else:
            mis_pelotas[i].establecer_distancia(distancia_2)
    numero = len(mis_pelotas)
    i= 0
    while (i < numero):
        j = i
        while (j < numero):
            if(mis_pelotas[i].consultar_distancia() < mis_pelotas[j].consultar_distancia()):
                temp = mis_pelotas[i]
                mis_pelotas[i] = mis_pelotas[j]
                mis_pelotas[j] = temp
            j= j+1
        i=i+1
    i=0
    y=0
    for i in mis_pelotas:
        generar_mapa()
        meta = mis_pelotas[i].consultar_posicion(1)
        camino= mi_mapa.camino_de_a( origen , meta)
        if mis_pelotas[i].consultar_posicion(2) is camino:
            camino.pop(mis_pelotas[i].consultar_posicion(2))
        origen = mis_pelotas[i].consultar_posicion(2)
        for w in range(0,len(camino)):
            misi.append(camino[w])
        del camino[:]
        generar_mapa()
    camino= mi_mapa.camino_de_a( origen , 'ho')
    if ' ' in misi:
        misi.remove(' ')
    for w in range(0,len(camino)):
        misi.append(camino[w])
    lon=len(misi)-1
    ori=360
    for i in range(0,lon):
        futuro=i+1
        ca=mi_mapa.consultar_orientacion(misi[i], misi[futuro])
        pe=ca-ori
        if pe < -180:
            pe+=360
        elif pe >180:
            pe-=360
        misio.append(pe)
        ori=ca
    if 'G6' in misi:
        eli=misi.index('G6')
        misi.pop(eli)
        misio.pop(eli)
        print (eli)
    if 'G4' in misi:
        eli=misi.index('G4')
        misi.pop(eli)
        misio.pop(eli)
    msgeme("Caminos:\n"+str(misi)+"\n"+str(misio))





orientaciones=[
    [['C1',360],['in',90]],#A1
    [['E1',360],['C2',90],['A1',180]],#C1
    [['E2',90],['C1',180]],#E1
    [['G1',360],['F2',90]],#F1
    [['G2',90],['F1',180]],#G1
    [['C2',360],['B5',90]],#B2
    [['D2',360],['B2',180],['C1',270]],#C2
    [['D3',90],['C2',180]],#D2
    [['F2',360],['E3',90],['E1',270]],#E2
    [['F3',90],['E2',180],['F1',270]],#F2
    [['H2',360],['G1',270]],#G2
    [['H3',90],['G2',180]],#H2
    [['E3',360],['D4',90],['D2',270]],#D3
    [['D3',180],['E2',270]],#E3
    [['H3',340],['F5',90],['F2',260]],#F3
    [['H6',90],['F3',150],['H2',270]],#H3
    [['E4',360],['D5',90],['D3',270]],#D4
    [['E5',90],['D4',180]],#E4
    [['G5',90]],#G4
    [['A1',270]],#in
    [['C5',360],['B2',270]],#B5
    [['D5',360],['C6',90],['B5',180]],#C5
    [['C5',180],['D4',270]],#D5
    [['F5',360],['E6',90],['E4',270]],#E5
    [['G5',360],['F6',90],['E5',180],['F3',270]],#F5
    [['F5',180],['G4',270]],#G5
    [['C6',360]],#ho
    [['E6',360],['ho',180],['C5',270]],#C6
    [['F6',360],['C6',180],['E5',270]],#E6
    [['E6',180],['F5',270]],#F6
    [['H6',360]],#G6
    [['G6',180],['H3',270]],#H6
    ]

adj=[
    ['in','A1',330],
    ['A1','C1',120],
    ['C1','C2',50],
    ['C2','B2',60],
    ['B2','B5',260],
    ['B5','C5',60],
    ['C5','D5',50],
    ['D5','D4',120],
    ['D4','D3',50],
    ['D3','D2',120],
    ['D2','C2',50],
    ['C1','E1',120],
    ['E1','E2',50],
    ['E2','F2',50],
    ['F2','F1',50],
    ['F1','G1',60],
    ['G1','G2',50],
    ['G2','H2',60],
    ['H2','H3',50],
    ['H3','H6',270],
    ['H6','G6',90],
    ['H3','F3',130],
    ['F2','F3',100],
    ['E2','E3',120],
    ['F3','F5',170],
    ['E4','E5',170],
    ['F5','G5',50],
    ['G5','G4',100],
    ['F5','F6',50],
    ['F5','E5',50],
    ['E5','E6',50],
    ['E6','F6',50],
    ['E6','C6',120],
    ['C5','C6',60],
    ['E4','D4',50],
    ['E3','D3',50],
    ['C6','ho',80]
    ]

cruces = [
    'A1',
    'C1',
    'E1',
    'F1',
    'G1',
    'B2',
    'C2',
    'D2',
    'E2',
    'F2',
    'G2',
    'H2',
    'D3',
    'E3',
    'F3',
    'H3',
    'D4',
    'E4',
    'G4',
    'in',
    'B5',
    'C5',
    'D5',
    'E5',
    'F5',
    'G5',
    'ho',
    'C6',
    'E6',
    'F6',
    'G6',
    'H6'
    ]


pcrucce = [
    [35, 455],#A1
    [35, 330],#C1
    [35, 230],#E1
    [35, 170],#F1
    [35, 105],#G1
    [90, 390],#B2
    [100, 330],#C2
    [100, 280],#D2
    [100, 230],#E2
    [100, 170],#F2
    [100, 105],#G2
    [100, 45],#H2
    [189, 280],#D3
    [195, 230],#E3
    [195, 170],#F3
    [165, 45],#H3
    [252, 280],#D4
    [250, 230],#E4
    [260, 110],#G4
    [370, 460],#in
    [370, 390],#B5
    [365, 330],#C5
    [370, 280],#D5
    [368, 225],#E5
    [368, 170],#F5
    [370, 115],#G5
    [440, 460],#ho
    [435, 330],#C6
    [433, 225],#E6
    [433, 170],#F6
    [433, 135],#G6
    [433, 45],#H6
    ]

posiciones = [
    [210, 460],#0
    [30, 390],#1
    [58, 330],#2
    [85, 368],#3
    [230, 390],#4
    [360, 360],#5
    [360, 305],#6
    [320, 280],#7
    [210, 280],#8
    [135, 280],#9
    [85, 305],#10
    [30, 277],#11
    [58, 230],#12
    [85, 204],#13
    [58, 175],#14
    [30, 145],#15
    [58, 105],#16
    [85, 80],#17
    [122, 45],#18
    [290, 45],#19
    [425, 90],#20
    [165, 105],#21
    [135, 175],#22
    [135, 230],#23
    [290, 175],#24
    [320, 230],#25
    [360, 145],#26
    [310, 115],#27
    [390, 175],#28
    [360, 200],#29
    [390, 230],#30
    [425, 204],#31
    [425, 277],#32
    [390, 330],#33
    [240, 258],#34
    [185, 258],#35
    [420, 370],#36
    ]


def main():
    global mi_mapa
    global mis_pelotas
    global num
    global CheckVar
    misi=[' ']
    misio=[]
    posicion_pelotas=[]
    mis_pelotas={}
    mi_mapa = m.mapa()

    generar_mapa()
    x=0
    for i in orientaciones:
        for j in i:
            c=cruces[x]
            eje=j[0]
            grados=j[1]
            mi_mapa.agregar_orientacion(c, eje, grados)
        x+=1
    top = tkinter.Tk()
    mapa = PhotoImage(file="mapa.gif")
    w1 = Label(top, image=mapa, bg="white")
    B = tkinter.Button(top, text ="Trazar", command = generar_camino)
    Bo = tkinter.Button(top, text ="enviar", command = mandar)
    Bc = tkinter.Button(top, text ="calibrar", command = cali)
    Bi = tkinter.Button(top, text ="iniciar", command = ini)
    LC={}
    for i in range(0,32):
        LC[i]= Label(top, text=cruces[i], fg="white", bg = "black")
        LC[i].pack()
        LC[i].place(bordermode=INSIDE, height=20, width= 20, x= pcrucce [i][0] ,y = pcrucce [i][1] )
    CheckVar={}
    L={}
    num = Label(top, bg = "white")
    for i in range(0, 37):
        CheckVar[i] = IntVar()
        texto = "L" + str(i)
        L[i]=Checkbutton(top, text = texto, variable = CheckVar[i], \
                         onvalue = 1, offvalue = 0, height=20, \
                         width = 30, command = sel, bg = "white")
        L[i].pack()
        L[i].place(bordermode=INSIDE, height=15, width= 40, x= posiciones [i][0] ,y = posiciones [i][1] )
    num.pack()
    w1.pack()
    B.pack()
    Bo.pack()
    num.place(bordermode=INSIDE, height=250 ,width= 135, x= 496 ,y = 10 )
    B.place(bordermode=INSIDE, height=50 ,width= 50, x= 525 ,y = 300 )
    Bo.place(bordermode=INSIDE, height=50 ,width= 50, x= 525 ,y = 350 )
    Bc.place(bordermode=INSIDE, height=50 ,width= 50, x= 525 ,y = 400 )
    Bi.place(bordermode=INSIDE, height=50 ,width= 50, x= 525 ,y = 450 )
    top.iconbitmap('bunny.ico')
    top.title("Control de mision Bunny")
    top.resizable(0,0)
    top.mainloop()

if __name__ == "__main__":
    main()