# -*- coding: utf-8 -*-
class pelota:

    def __init__(self, nodo_1, nodo_2):
        self.posicion_uno = nodo_1
        self.posicion_dos = nodo_2
        self.distancia = 0
        self.prioridad = 0
        self.asegurada= False
        self.camino={}

    def consultar_posicion(self,p):
        if p == 1:
            return self.posicion_uno
        if p == 2:
            return self.posicion_dos

    def establecer_distancia(self, distancia):
        self.distancia = distancia

    def consultar_distancia(self):
        return self.distancia

    def esta_asegurada(self):
        return self.asegurada

    def asegurado(self):
        self.asegurado = True
        return self.aseurado

    def estatablecer_prioridad(self, prio):
        self.prioridad = prio

    def consultar_prioridad(self):
        return self.prioridad





