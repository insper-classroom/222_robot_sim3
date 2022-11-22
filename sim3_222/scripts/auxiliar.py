#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Atenção: usado no notebook da aula. 
    Não precisa ser usado diretamente
"""

import numpy as np
import cv2

import os
print("Trabalhando em ", os.getcwd())


def center_of_mass(data):
    """ 
        Retorna uma tupla (cx, cy) que desenha o
        centro de data, que pode ser contorno ou matriz
    """
    M = cv2.moments(data)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (int(cX), int(cY))

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

font = cv2.FONT_HERSHEY_SIMPLEX
def texto(img, a, p, color=(0, 255, 255), font=font, width=2, size=1):
    """
        Escreve na img RGB
        dada a string a na posição
        definida pela tupla p
    """
    cv2.putText(img, str(a), p, font,size,color,width,cv2.LINE_AA)

# Analises dos canais:
def hsv_hists(img, plt):
    """
        Plota o histograma de cada um dos canais HSV
        img - imagem HSV
        plt - objeto matplotlib
    """
    plt.figure(figsize=(20,10));
    img_h = img[:,:,0]
    img_s = img[:,:,1]
    img_v = img[:,:,2]
    histo_plot(img_h, "r","H", plt);
    histo_plot(img_s, "g","S", plt);
    histo_plot(img_v, "b","V", plt);

def make_hist(img_255, c, label, plt):
    """ img_255 - uma imagem com 3 canais de 0 até 255
        c a cor do plot
        label - o label do gráfico
        plt - matplotlib.pyplot
    """
    hist,bins = np.histogram(img_255.flatten(),256,[0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max()/ cdf.max()

    # plt.plot(cdf_normalized, color = c)
    plt.hist(img_255.flatten(),256,[0,256], color = c)
    plt.xlim([0,256])
    plt.legend(label, loc = 'upper left')
    plt.plot()

def histo_plot(img, cor, label, plt):
    """
        img - imagem
        cor - cor
        plt - matplotlib.pyplot object
    """
    plt.figure(figsize=(10,5))
    make_hist(img, cor, label, plt)
    plt.show()
    plt.figure(figsize=(10,5))
    plt.imshow(img, cmap="Greys_r")#, vmin=0, vmax=255)
    plt.title(label)

if __name__ == "__main__":
	print("Este script não deve ser executado diretamente")

