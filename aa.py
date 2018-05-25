
import serial

disponibles = []

for i in range(10):
    try:
        s = serial.Serial(i)
        disponibles.append((i, s.portstr))
        s.close()
    except:
        pass

print "Puertos disponibles: "
for numpuerto,nombre in disponibles:
    print "%d -> %s" % (numpuerto, nombre)