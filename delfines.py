import numpy as np
import networkx as nx
import matplotlib.pylab as plt
from urllib.request import urlopen
from random import shuffle
from copy import deepcopy


red_delf = nx.read_gml(urlopen("https://raw.githubusercontent.com/MarianoNicolini17/TP1/master/Datos/dolphins.gml"))
gen_delf = urlopen("https://raw.githubusercontent.com/MarianoNicolini17/TP1/master/Datos/dolphinsGender.txt").readlines()

for i in range(len(gen_delf)):
    gen_delf[i]=gen_delf[i].decode()
    
sex_delf = []   
for i in range(len(gen_delf)):
    a = gen_delf[i].rstrip('\n').split('\t')
    sex_delf.append(a)
    
    
# -----------------------------------------------------------------------------

def atributoNodos(r, alist, atributo):
# Toma como argumentos una red, una lista de listas, donde cada una de ellas
# indica el atributo que se le va a asignar a cada nodo de la red. Devuelve la
# red con ese atributo ya asociado.
    for idx, nodo in enumerate(np.array(alist).transpose()[0]):
        r.nodes[nodo][atributo] = np.array(alist).transpose()[1][idx]
    
# ----------------------------------------------------------------------------- 
        
def contadorGenero(r):
    a = list(nx.get_node_attributes(r, 'gender').values())
    return a.count('m'), a.count('f'), a.count('NA')

# -----------------------------------------------------------------------------
    
def generoAzar(r):
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
            
def nulaAtributo(r, atributo, pasos):
    a = []
    for i in range(pasos):
        ra = generoAzar(r)
        a.append(hEdges(ra, 'gender'))
    lhomo = np.array(a).transpose()[0]
    lhetero = np.array(a).transpose()[1]
    return lhomo, lhetero
        
    


    
    
atributoNodos(red_delf, sex_delf, 'gender')    
    
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