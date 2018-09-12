import numpy as np
import networkx as nx
import matplotlib.pylab as plt
from urllib.request import urlopen


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

def atributosDelf(delfnx, alist, atributo):
# Toma como argumentos una red, una lista de listas, donde cada una de ellas
# indica el atributo que se le va a asignar a cada nodo de la red. Devuelve la
# red con ese atributo ya asociado.
    for idx, delf in enumerate(np.array(alist).transpose()[0]):
        delfnx.nodes[delf]['gender'] = np.array(alist).transpose()[1][idx]
    
# -----------------------------------------------------------------------------    
    
atributosDelf(red_delf, sex_delf, 'gender')    
    
graph_pos=nx.spring_layout(red_delf)


#plt.figure(figsize=(20,10))

nx.draw_networkx_nodes(red_delf, graph_pos, node_size=10, node_color='blue', alpha=0.3)
nx.draw_networkx_edges(red_delf, graph_pos)
nx.draw_networkx_labels(red_delf,graph_pos, font_size=8, font_family='sans-serif')

plt.savefig("plot.png", dpi=1000)
plt.show()