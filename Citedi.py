# -*- coding: utf-8 -*-
"""
Created on Sat May 19 20:47:46 2018

@author: Angel
"""
from Navegacion import mapa as m
from Navegacion import brujula as b
import pelotas as p


def generar_mapa():
    global mi_mapa
    for i in cruces:
        mi_mapa.definir_nodo(i)
    for i in adj:
        mi_mapa.agregar_distancia(i[0],i[1], i[2])
        
def generar_camino():
    global mis_pelotas
    global misi
    global misio
    misi=[' ']
    misio=[]
    generar_mapa()
    
    #saco del mapa las distancias de los nodos de la linea sobre la que esta la pelota, y eligo el de menor distancia.
    origen = '31'
    for i in mis_pelotas:
        distancia_1 = mi_mapa.distancia_entre('31', mis_pelotas[i].consultar_posicion(1))
        generar_mapa()
        distancia_2 = mi_mapa.distancia_entre('31', mis_pelotas[i].consultar_posicion(2))
        if distancia_1 <= distancia_2:
            mis_pelotas[i].establecer_distancia(distancia_1)
        else:
            mis_pelotas[i].establecer_distancia(distancia_2)
    numero = len(mis_pelotas)
     ##algoritmo de borbuja para organizar las pelostas, de la mas cercanas a la mas lejanas
     
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
  # comienza la busqueda de las pelotas en el mapa.
    for i in mis_pelotas:
        generar_mapa()
        meta = mis_pelotas[i].consultar_posicion(1)
        camino= mi_mapa.camino_de_a( origen , meta)
        # si la ruta trasada pasa por el nodo pero no por la linea 
        # se toma el otro nodo de la linea de la pelota y se agrega al camino resultante
        if mis_pelotas[i].consultar_posicion(2) is camino:
            camino.pop(mis_pelotas[i].consultar_posicion(2))
        origen = mis_pelotas[i].consultar_posicion(2)
        
        for w in range(0,len(camino)):
            misi.append(camino[w])
        del camino[:]
        generar_mapa()
        
    camino= mi_mapa.camino_de_a( origen , '31')
    if ' ' in misi:
        misi.remove(' ')
    for w in range(0,len(camino)):
        misi.append(camino[w])
    lon=len(misi)-1
    ori=90
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
#    if 'G6' in misi:
#        eli=misi.index('G6')
#        misi.pop(eli)
#        misio.pop(eli)
#        print (eli)
#    if 'G4' in misi:
#        eli=misi.index('G4')
#        misi.pop(eli)
#        misio.pop(eli)
   # msgeme("Caminos:\n"+str(misi)+"\n"+str(misio))

cruces= [
    '11',
    '12',
    '13',
    '14',
    '15',
    '21',
    '22',
    '23',
    '24',
    '25',
    '31',
    '32',
    '33',
    '34',
    '35',
    '41',
    '42',
    '43',
    '44',
    '45',
    '51',
    '52',
    '53',
    '54',
    '55'
    ]

adj=[
    ['11','12',30],
    ['12','13',30],
    ['13','14',30],
    ['14','15',30],
    ['11','21',30],
    ['12','22',30],
    ['13','23',30],
    ['14','24',30],
    ['15','25',30],
    ['21','22',30],
    ['22','23',30],
    ['23','24',30],
    ['24','25',30],
    ['21','31',30],
    ['22','32',30],
    ['23','33',30],
    ['24','34',30],
    ['25','35',30],
    ['31','32',30],
    ['32','33',30],
    ['33','34',30],
    ['34','35',30],
    ['31','41',30],
    ['32','42',30],
    ['33','43',30],
    ['34','44',30],
    ['35','45',30],
    ['41','42',30],
    ['42','43',30],
    ['43','44',30],
    ['44','45',30],
    ['41','51',30],
    ['42','52',30],
    ['43','53',30],
    ['44','54',30],
    ['45','55',30],
    ['51','52',30],
    ['52','53',30],
    ['53','54',30],
    ['54','55',30]
    ]

orientaciones=[
    [['21',360],['12',90]],#11
    [['22',360],['13',90],['11',270]],#12
    [['23',360],['14',90],['12',270]],#13
    [['24',360],['15',90],['13',270]],#14
    [['25',360],['14',270]],#15
    [['31',360],['22',90],['11',180]],#21
    [['32',360],['23',90],['12',180],['21',270]],#22
    [['33',360],['24',90],['13',180],['22',270]],#23
    [['34',360],['25',90],['14',180],['23',270]],#24
    [['35',360],['15',180],['24',270]],#25
    [['41',360],['32',90],['21',180],['ini',270]],#31
    [['42',360],['33',90],['22',180],['31',270]],#32
    [['43',360],['34',90],['23',180],['32',270]],#33
    [['44',360],['35',90],['24',180],['33',270]],#34
    [['45',360],['25',180],['34',270]],#35
    [['51',360],['42',90],['31',180]],#41
    [['52',360],['43',90],['32',180],['41',270]],#42
    [['53',360],['44',90],['33',180],['42',270]],#43
    [['54',360],['45',90],['34',180],['43',270]],#44
    [['55',360],['35',180],['44',270]],#45
    [['52',90],['41',180]],#51
    [['53',90],['42',180],['51',270]],#52
    [['54',90],['43',180],['52',270]],#53
    [['55',90],['44',180],['53',270]],#54
    [['45',180],['54',270]]#55
    ]

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
    
global nodos_a_eliminar #los nodos a eliminar
global posiciones_a_eliminar# se guardan el index de los elementos a eliminar

def eliminar_nodos():
    nodos_a_eliminar
    posiciones_a_eliminar
    for i in nodos_a_eliminar:
       posiciones_a_eliminar=cruces[i].index(nodos_a_eliminar[i])
        