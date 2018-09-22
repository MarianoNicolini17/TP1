# Punto 3 del TP 1 de redes.
#
# Este archivo utiliza una librería llamada "powerlaw", con métodos para fitear
# power-law y otras funciones a los datos, usando loglikelihood y el test de
# Kolmogorov-Smirnov para obtener el k mínimo.
#
# Para instalar la librería usando pip:
#                               pip install powerlaw
#
# Más información en https://github.com/jeffalstott/powerlaw.
#
# Referencia:
# Jeff Alstott, Ed Bullmore, Dietmar Plenz. (2014). powerlaw: a Python package 
# for analysis of heavy-tailed distributions. PLoS ONE 9(1): e85777

import networkx as nx
from urllib.request import urlopen
import numpy as np
import matplotlib.pylab as plt
import powerlaw as pl
from os import listdir

# - Chequea si está el archivo con los datos en donde debería estar, y si no
#   lo saca de la web.
# ~ Sasha

if "as-22july06.gml" not in listdir('Datos/'):
    red_auto = nx.read_gml(urlopen("https://raw.githubusercontent.com/MarianoNicolini17/TP1/master/Datos/as-22july06.gml"))
else:
    red_auto = nx.read_gml("Datos/as-22july06.gml")

#------------------------------------------------------------------------------

x = np.array(list(dict(red_auto.degree).values()))
# - Descarté la función grados() para usar directamente métodos de python.
#   Ahora el tiempo de ejecución es mucho más corto.
# ~ Sasha

logbins = np.logspace(np.log10(np.min(x)), np.log10(np.max(x)), num=10)
# Esta variable es una lista que va a servir para setear que los bines del 
# histograma tengan un espaciado logarítmico.

#------------------------------------------------------------------------------

# Diferentes maneras de visualizar el histograma de la distribución de
# grado de la red.

# - Acá dejo una alternativa para plotear con puntos. Creo que es un poco más
#   claro para bins con probabilidad chiquita. Además, se nota claramente el
#   efecto "plateau" en el log-log con binning lineal.
#
# - Histogramas normalizados.
#
# - Para los plots log-log uso directamente el método de la librería powerlaw,
#   porque binea automáticamente y me gusta bastante cómo quedó. A pesar de
#   que el bineo logarítmico de 10 de Marian queda más lindo, que se vean 
#   irregularidades no es necesariamente algo malo!
#
# - Agrego la CDF y la CCDF, que vienen con la librería.
#
# - Si hay algo que les parece que estaba mejor antes, no hay ningún problema
#   porque se vuelve!
#
# ~ Sasha

N = len(x)

# Distribución de grado en escala lin-lin, bineado lineal.
plt.figure(figsize=(10,10))
linlinc, bin_edges = np.histogram (x,100)
linlinb = (bin_edges[:-1] + bin_edges[1:])/2. # Punto en el centro del bin.
plt.plot(linlinb,linlinc/N,'bo')
plt.title("Distribución de grado de la red (lin-lin)")
plt.show()

# Distribución de grado en escala log-lin, bineado lineal.
plt.figure(figsize=(10,10))
loglinc, bin_edges = np.histogram (x,300)
loglinb = (bin_edges[:-1] + bin_edges[1:])/2.
plt.plot(loglinb,loglinc/N,'bo')
plt.xscale("log")
plt.title("Distribución de grado de la red (log-lin)")
plt.show()

# Distribución de grado en escala log-log, bineado lineal.
plt.figure(figsize=(10,10))
plt.title("Distribución de grado de la red (log-log)")
pl.plot_pdf(x, linear_bins=True, color='b', marker="o", linestyle='None')

# Distribución de grado en escala log-log, bineado logarítmico.
plt.figure(figsize=(10,10))
plt.title("Distribución de grado de la red (log-log, bineo logarítmico)")
pl.plot_pdf(x, color='b', marker="o", linestyle='None')

# CDF del grado en escala log-log.
plt.figure(figsize=(10,10))
plt.title("CDF de la red (log-log)")
pl.plot_cdf(x, color='b', marker="o", linestyle='None')

# CCDF del grado en escala log-log.
plt.figure(figsize=(10,10))
plt.title("CCDF de la red (log-log)")
pl.plot_ccdf(x, color='b', marker="o", linestyle='None')

#------------------------------------------------------------------------------

# Faltaría agregar una discusión de por qué conviene más usar escala log-log
# con bineo logarítmico. El argumento está en el tópico avanzado B del capítulo 4
# de Barabasi. Igual, es bastante claro.
# ~ Sasha.

#------------------------------------------------------------------------------

# - fit es un objeto que guarda toda la información de los datos y el fiteo
# apenas se lo crea con pl.Fit(data,...). De hecho, se puede acceder a (en
# principio) cualquier fiteo que se quiera. Para acceder al de power law
# (y todos los parámetros del ajuste) se usa fit.power_law.
#
# - La opción discrete=True es necesaria porque los datos de grado toman sólo
#   valores discretos.
#
# - Podría agregarse la comparación con otros ajustes como manera de evaluar el
#   goodness-of-fit.
#
# ~ Sasha

# Esta línea es porque tira un par de warnings medios raros :S. Hay que ver si
# importan o no (dice que divide por cero y por cantidad inválida, algo así).
np.seterr(divide='ignore',invalid='ignore')

fit = pl.Fit(x,discrete=True,verbose=False)
plt.figure(figsize=(10,10))
fig = fit.plot_pdf(color='b', linestyle='None', marker='o')
fit.power_law.plot_pdf(color='r', linestyle='--', ax=fig)
fig.figure

print ("El valor del exponente según la aproximación es de", \
       fit.power_law.alpha)
print ("El k mínimo obtenido para la mínima distancia de", \
       "Kolmogorov-Smirnov:", fit.power_law.xmin)
print ("La mínima distancia de Kolmogorov-Smirnov es:", fit.power_law.D)

#------------------------------------------------------------------------------