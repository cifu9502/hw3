from __future__ import division 
import numpy as np

from scipy import meshgrid
import matplotlib.pyplot as plt

part = 250 

#recupera la informacion de la matriz  Matrix guardada en filename
#inputs fileName-- nombre del archivo donde se guarda
#       matix--  matriz a guaradar
#       dim-- dimension de la matriz

def cargar(fileName,dim):
    infile = open(fileName, 'r')
    
    #load the full text by lines
    text = infile.readlines()
    
    ro1 = np.zeros((dim, dim,dim))
    num = 1
    for i in range(0,dim):
        for j in range(0,dim):
             g = text[num].split(',')
             g = np.array(g[:-1])
             ro1[i,j,:]= g.astype(np.float)
             num = num+1
    return ro1            




#Grafica la imagen 


ro = cargar('densidades.dat',part)
F2 = cargar('fuerza.dat',part-2)

#Obtiene minimos y maximos
mini = F2.min()
Max = F2.max()

#Se fijan los valores minimos y maximos en x,y y z de la posicion, estos se obtienen de los valores minimos y maximos en cada vector p[0] 
#p[1], p[2] definido en el archivo de ipython
minx = 33.85371
maxx = 36.568359999999998
miny = 33.923020000000001
maxy = 36.650640000000003
minz = 33.495959999999997
maxz = 36.909080000000003

#Da la posicision en 3D del elemento senalado en la matriz F2 de fuerzas
def darPosicion(num):
    for i in range(0,part-2):
        for j in range(0,part-2):
            for k in range(0,part-2):
                if F2[i,j,k] == num:
                    #Se transforma a nuestras coordenadas
                    i1 = i*(maxx-minx)/part + minx
                    j1 = j*(maxy-miny)/part + miny
                    k1 = k*(maxz-minz)/part + minz
                    return [i1,j1,k1]
                     
mi = darPosicion(mini)           
maxi = darPosicion(Max)

print "El punto de minima fuerza es " + repr(mi)
print "El punto de maxima fuerza es " + repr(maxi)


#Proyectamos al plano x-z  para graficar (Esto es, sumamos sobre cada punto en el plano x-z las fuerzas para cada posicion en y)
F12 = F2[:,0,:]
for k in range(1, part-2):
    F12 = F12 + F2[:,k,:]

#Da la posicision en 3D del elemento senalado en la matriz F12 de fuerzas proyectadas al plano x-z
def darPosicion2(num):
    for i in range(0,part-2):
        for j in range(0,part-2):
            if F12[i,j] == num:
                i1 = i*(maxx-minx)/part + minx
                j1 = j*(maxz-minz)/part + minz
                return [i1,j1]


mini = F12.min()
Max = F12.max()

#Se encuentra la posicion de los puntos de minima y maxima fuerza en el plano x-z utilizando la funcion darPosicion2
mi2 = darPosicion2(mini)           
maxi2 = darPosicion2(Max) 

print "Cuando proyectamos al plano x-z el punto de minima fuerza es " + repr(mi2)
print "Y el punto de maxima fuerza es " + repr(maxi2)   

#Se grafican los puntos de minima y maxima fuerza
plt.plot([mi2[0]], [mi2[1]], 'ro')
plt.text(mi2[0],mi2[1],'Minimo')


plt.plot([maxi2[0]], [maxi2[1]], 'ro')
plt.text(maxi2[0],maxi2[1],'Maximo')

#Se grafica la matriz F12 de fuerzas proyectadas al plano x-z. Note que el resultado es muy parecido a la imagen dada, fue por eso que se escogio este plano
#Se esta extendiendo entre los valores  minimos y maximos en x y en z en el archivo de ipython que  correponden justamente a los valores minimos y maximos de la posicion

plt.imshow(F12.T, extent=(minx, maxx,minz,maxz), origin='lower')
plt.title('Fuerzas en Serena Venus (plano x-z)')
plt.ylabel('Z')
plt.xlabel('X')
plt.savefig('serena.png')
plt.show()
