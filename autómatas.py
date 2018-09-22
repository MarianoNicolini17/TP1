import networkx as nx
from urllib.request import urlopen
import numpy as np
import matplotlib.pylab as plt


red_auto = nx.read_gml(urlopen("https://raw.githubusercontent.com/MarianoNicolini17/TP1/master/Datos/as-22july06.gml"))

#------------------------------------------------------------------------------

def grados(r):
# Toma como argumento una red y devuelve una lista con el grado de cada nodo de
# la red.
    a = []
    for key in dict(r.degree):
        a.append(dict(r.degree)[key])
    return a
 
#------------------------------------------------------------------------------
    
x = np.array(grados(red_auto)) #Tarda mucho en correr! La red es muy grande.

logbins = np.logspace(np.log10(np.min(x)), np.log10(np.max(x)), num=10)
# Esta variable es una lista que va a servir para setear que los bines del 
# histograma tengan un espaciado logarítmico.

#------------------------------------------------------------------------------

# Diferentes maneras de visualizar el histograma de la distribución de
# grado de la red.


#fig = plt.figure(figsize=(10,10))


# Distribución de grado en escala lin-lin, bineado lineal.
plt.hist(x, bins=100, density=True, log=False)
plt.title("Distribución de grado de la red")
plt.show()

# Distribución de grado en escala log-lin, bineado lineal.
plt.hist(x, bins=300, density=True, log=False)
plt.title("Distribución de grado de la red")
plt.xscale("log")
plt.show()


# Distribución de grado en escala log-log, bineado lineal.
plt.hist(x, bins=80, density=True, log=True)
plt.title("Distribución de grado de la red")
plt.xscale("log")
plt.show()

# Distribución de grado en escala log-log, bineado logarítmico.
plt.hist(x, bins=logbins, density=True, log=True)
plt.title("Distribución de grado de la red")
plt.xscale("log")
plt.show()

# Los números que usé para dividir los bines en los tres primeros los puse 
# después de probar varios números, no es nada definitivo. Pueden experimentar
# tranquilamente con otros números si quieren. El último quedó muy lindo!
