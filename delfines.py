import numpy as np
import networkx as nx
import matplotlib.pylab as plt
from urllib.request import urlopen
from random import shuffle


red_delf = nx.read_gml(urlopen("https://raw.githubusercontent.com/MarianoNicolini17/TP1/master/Datos/dolphins.gml"))
gen_delf = urlopen("https://raw.githubusercontent.com/MarianoNicolini17/TP1/master/Datos/dolphinsGender.txt").readlines()



for i in range(len(gen_delf)):
    gen_delf[i]=gen_delf[i].decode()
    
    
sex_delf = []   
for i in range(len(gen_delf)):
    a = gen_delf[i].rstrip('\n').split('\t')
    sex_delf.append(a)
    

for idx, delf in enumerate(np.array(sex_delf).transpose()[0]):
    red_delf.nodes[delf]['gender'] = np.array(sex_delf).transpose()[1][idx]
    
# -----------------------------------------------------------------------------

def atributoNodos(nx, alist, atributo):
# Toma como argumentos una red, una lista de listas, donde cada una de ellas
# indica el atributo que se le va a asignar a cada nodo de la red. Devuelve la
# red con ese atributo ya asociado.
    for idx, nodo in enumerate(np.array(alist).transpose()[0]):
        nx.nodes[nodo][atributo] = np.array(alist).transpose()[1][idx]
    
# ----------------------------------------------------------------------------- 
        
        
def contadorGenero(r):
    a = list(nx.get_node_attributes(r, 'gender').values())
    return a.count('m'), a.count('f'), a.count('NA')
    
def generoAzar(r):
    nX = contadorGenero(r)
    n = list(r.nodes)
    shuffle(n)
    for i in range(nX[0]):
        r.nodes[n[i]]['gender'] = 'm'
    for i in range(nX[0], nX[0]+nX[1]):
         r.nodes[n[i]]['gender'] = 'f'
    for i in range(nX[0]+nX[1], nX[0]+nX[1]+nX[2]):
         r.nodes[n[i]]['gender'] = "NA"
    return r
        

    
atributoNodos(red_delf, sex_delf, 'gender')    
    
graph_pos=nx.spring_layout(red_delf)


plt.figure(figsize=(20,20))

nx.draw_networkx_nodes(red_delf, graph_pos, node_size=50,
                       node_color = ["blue" if g=="m" else "red" if g=="f" else \
                                     "yellow" for g in nx.get_node_attributes(red_delf, 'gender').values()],
                       alpha=0.5)
nx.draw_networkx_edges(red_delf, graph_pos)
#nx.draw_networkx_labels(red_delf,graph_pos, font_size=8, font_family='sans-serif')

plt.savefig("plot.png", dpi=1000)
plt.show()