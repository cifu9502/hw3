# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>
from __future__ import division
from mpl_toolkits.basemap import Basemap

# <codecell>


import numpy as np
import string


from matplotlib import pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy import interpolate

#archivo a leer
s = 'coastal-stns-byVol-updated-oct2007.txt'


#Se lee el archivo
infile = open(s, 'r')
text = infile.readlines()
#En vec se guardaran las lineas del texto en una forma mucho mas leible
vec = []
#flux sera el vector de flujos
flux = []
for x in text:
    #parte el texto x segun ' '
    a = x.split(' ')
    n = 0
    for y in x.split(' '):
        #omite los residuos de la forma ''
        if(y == ''):
            a.pop(n)
            n = n-1
        if((n == 5) & (y != '')& (y != 'Vol(km3/yr)')):
            flux.append(float(y))
        n = n+1
    vec.append(a)    
titulos = vec.pop(0)

#Se extraen las latitudes, longitudes, nombre y flujo de los 150 rios con mayor flujo
lats = []
lons = []
name = []
f = []
for i in range(0,159):
    #se encuentra el maximo de los flujos y luego se busca la linea que contenga este flujo
    m = max(flux)
    i = 0
    for v in vec:
        if flux[i] == m:
            f.append(m)
            lons.append(float(v[2]))
            lats.append(float(v[3]))
            name.append(v[12])
            flux.remove(m)
            vec.remove(v)
            break
        i = i +1
        

# <codecell>



from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#se inicia basemap
fig = plt.figure()
m = Basemap(projection='hammer',lon_0=0) 

#Cada rio se grafica en el mapa usando su latitud y longitud, debido al espacio disponible en la grafica solo se pone el
#nombre en los primeros 10 rios
for i in range(0, len(lats)):
    xpt,ypt = m(lons[i],lats[i])
    lonpt, latpt = m(xpt,ypt,inverse=True)
    m.plot(xpt,ypt,'ro') 
    if i < 11:
        plt.text(xpt+100000,ypt+100000,name[i] + "(" +repr(f[i]) + ")")


m.drawmapboundary(fill_color='#99ffff')
m.fillcontinents(color='#cc9966',lake_color='#99ffff')
plt.title('Rios con mayor flujo (150)')
plt.savefig('150riosMapa.png')
plt.show()

# <codecell>


