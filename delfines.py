import numpy as np
import networkx as nx
import matplotlib.pylab as plt
from urllib.request import urlopen
from random import shuffle
from copy import deepcopy

# Acá se guardan los datos que vamos a usar.

red_delf = nx.read_gml(urlopen("https://raw.githubusercontent.com/MarianoNicolini17/TP1/master/Datos/dolphins.gml"))
gen_delf = urlopen("https://raw.githubusercontent.com/MarianoNicolini17/TP1/master/Datos/dolphinsGender.txt").readlines()

#------------------------------------------------------------------------------

# Ésta parte del código es para generar la lista de listas que asocia cada nodo
# de la red de delfines con un atributo. Después de ejecutarlo van a tener una 
# lista de listas que se llama sex_delf. Es la lista que tienen que usar 
# después con la función atributoNodos para que le asigne esos atributos a
# red_delf.

for i in range(len(gen_delf)):
    gen_delf[i]=gen_delf[i].decode()
    
sex_delf = []   
for i in range(len(gen_delf)):
    a = gen_delf[i].rstrip('\n').split('\t')
    sex_delf.append(a)
    
# -----------------------------------------------------------------------------

def atributoNodos(r, alist, atributo):
# Toma como argumentos una red, una lista de listas, donde cada una de ellas
# indica el atributo que se le va a asignar a cada nodo de la red, y el 
# atributo que uno quiere asignar. Devuelve la red con ese atributo ya asociado
# a cada nodo.
    for idx, nodo in enumerate(np.array(alist).transpose()[0]):
        r.nodes[nodo][atributo] = np.array(alist).transpose()[1][idx]

atributoNodos(red_delf, sex_delf, 'gender') 
    
# ----------------------------------------------------------------------------- 
        
def contadorGenero(r): #Generalizarlo para cualquier atributo
    a = list(nx.get_node_attributes(r, 'gender').values())
    return a.count('m'), a.count('f'), a.count('NA')

# -----------------------------------------------------------------------------
    
def generoAzar(r):
# Toma una red donde sus nodos tienen el atributo "genero" y lo distribuye al
# azar. 
# Estaría bueno generalizarlo después para cualquier atributo.
    ng = contadorGenero(r)
    n = list(r.nodes)
    shuffle(n)
    ra = deepcopy(r)
    for i in range(ng[0]):
        ra.nodes[n[i]]['gender'] = 'm'
    for i in range(ng[0], ng[0]+ng[1]):
         ra.nodes[n[i]]['gender'] = 'f'
    for i in range(ng[0]+ng[1], ng[0]+ng[1]+ng[2]):
         ra.nodes[n[i]]['gender'] = "NA"
    return ra

# -----------------------------------------------------------------------------

def hEdges(r, atributo):
# Recibe como argumentos una red y un cierto atributo (str) para el cual se 
# quiere ver cuántos enlaces hay entre nodos con el mismo atributo y
# cuántos entre nodos con atributos diferentes.
# Devuelve una tupla de dos números, en el primer lugar la cantidad de enlaces
# entre nodos del mismo atributo y en el segundo entre nodos de atributos 
# diferentes.
    homo = 0
    hetero = 0
    for i in range(len(list(r.edges))):
        if r.nodes[a[i][0]][atributo] == r.nodes[a[i][1]][atributo]:
            homo += 1
        else:
            hetero += 1
    return homo, hetero
            
# -----------------------------------------------------------------------------            
            
def nulaAtributo(r, pasos): # Generalizarlo para cualquier atributo.
# Recibe como argumento una red y una cantidad de pasos sobre los cuales se va
# a iterar.
# Devuelve dos arrays, una con el número de enlaces homofílicos y otra con el 
# número de enlaces heterofílicos, para cada red creada al azar.
    a = []
    for i in range(pasos):
        ra = generoAzar(r)
        a.append(hEdges(ra, 'gender'))
    lhomo = np.array(a).transpose()[0]
    lhetero = np.array(a).transpose()[1]
    return lhomo, lhetero
   
atributoNodos(red_delf, sex_delf, 'gender') 
     
# -----------------------------------------------------------------------------    

def intersect(l1, l2): 
# Intersección entre dos listas.
    l3 = [value for value in l1 if value in l2] 
    return l3

def overlapOrdenado(r):
# Recibe una red y devuelve una lista de listas, donde cada una de ellas es un
# enlace, en el primer elemento, y el overlap de dicho enlace, en el segundo, 
# ordenadas según el overlap, de menor a mayor.
    a = []
    for enlace in list(r.edges):
        v1 = list(r.adj[enlace[0]])
        v2 = list(r.adj[enlace[1]])
        ni = len(intersect(v1,v2))
        nu = len(v1) + len(v2) - ni -2
        a.append([enlace, ni/nu])
    a.sort(key=lambda x: x[1]) # key=lambda me ordena la lista eligiendo algun
    return a                   # valor como criterio (el overlap en este caso)

# -----------------------------------------------------------------------------

# Esta parte del código es para graficar la red de delfines.
    
graph_pos=nx.spring_layout(red_delf)

#plt.figure(figsize=(20,20))
nx.draw_networkx_nodes(red_delf, graph_pos, node_size=50,
                       node_color = ["blue" if g=="m" else "red" if g=="f" else \
                                     "yellow" for g in nx.get_node_attributes(red_delf, 'gender').values()],
                       alpha=0.5)
nx.draw_networkx_edges(red_delf, graph_pos)
#nx.draw_networkx_labels(red_delf,graph_pos, font_size=8, font_family='sans-serif')

plt.savefig("plot.png", dpi=1000)
plt.show()

# -----------------------------------------------------------------------------

# Ésta parte del código es para hacer los histogramas de la hipótesis nula.

size = 10000
x1 = nulaAtributo(red_delf, size)[0]/red_delf.number_of_edges()
x2 = nulaAtributo(red_delf, size)[1]/red_delf.number_of_edges()


plt.hist(x1, bins='scott')
plt.title("Distribución nula de homofilia para {} muestras".format(size))
plt.show()

plt.hist(x2, bins='scott') 
plt.title("Distribución nula de heterofilia para {} muestras".format(size))
plt.show()

# Después de probar varias maneras de estimar el número de bins para el 
# histograma, encontré que la mejor es con bins='scott', cuando uso un 
# size = 10000. Para sizes más chicos no queda tan bien. Les dejo la página con
# la documentación de otras opciones para la cantidad de bins por si quieren
# probar:
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram_bin_edges.html#numpy.histogram_bin_edges
















