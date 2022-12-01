#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import math
import numpy as np

from sklearn.linear_model import (LinearRegression, RANSACRegressor)

def segmenta_linha_amarela(bgr):
    """Não mude ou renomeie esta função
        deve receber uma imagem bgr e retornar uma máscara com os segmentos amarelos do centro da pista em branco.
        Utiliza a função cv2.morphologyEx() para limpar ruidos na imagem
    """

    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mini = (45/2, 50, 50)
    maxi = (75/2, 255, 255)
    mask = cv2.inRange(hsv, mini, maxi)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN, np.ones((11,11),dtype=np.uint8))
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE, np.ones((11,11),dtype=np.uint8))

    return mask

def encontrar_contornos(mask):
    """Não mude ou renomeie esta função
        deve receber uma imagem preta e branca e retornar todos os contornos encontrados
    """
    contornos, arvore = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)   

    return contornos

def crosshair(img, point, size, color):
    """ Desenha um crosshair centrado no point.
        point deve ser uma tupla (x,y)
        color é uma tupla R,G,B uint8
    """
    x,y = point
    x = int(x)
    y = int(y)
    cv2.line(img,(x - size,y),(x + size,y),color,2)
    cv2.line(img,(x,y - size),(x, y + size),color,2)

def encontrar_centro_dos_contornos(bgr, contornos):
    """Não mude ou renomeie esta função
        deve receber uma lista de contornos e retornar, respectivamente,
        a imagem com uma cruz no centro de cada segmento e o centro de cada. 
        formato: img, x_list, y_list
    """

    img = bgr.copy()
    x_list = []
    y_list = []

    for contorno in contornos:
        M = cv2.moments(contorno)
        x = int(M["m10"]/M["m00"])
        y = int(M["m01"]/M["m00"])
        
        #x = int(contorno[:,:,0].mean())
        #y = int(contorno[:,:,1].mean())
        crosshair(img, (x,y), 5,(0,0,255))
        x_list.append(x)
        y_list.append(y)

    return img, x_list, y_list

def desenhar_linha_entre_pontos(bgr, X, Y, color):
    """Não mude ou renomeie esta função
        deve receber uma lista de coordenadas XY, e retornar uma imagem com uma linha entre os centros EM SEQUENCIA do mais proximo.
    """
    img = bgr.copy()
    x_ant = None
    y_ant = None
    for x, y in zip(X,Y) :
        if x_ant is not None:
            cv2.line(img, (x_ant, y_ant), (x,y),(0,0,255), thickness=2)
        x_ant = x
        y_ant = y

    return img

def regressao_por_centro(bgr, x_array, y_array):
    """Não mude ou renomeie esta função
        deve receber uma lista de coordenadas XY, e estimar a melhor reta, utilizando o metodo preferir, que passa pelos centros. Retorne a imagem com a reta e os parametros da reta
        
        Dica: cv2.line(img,ponto1,ponto2,color,2) desenha uma linha que passe entre os pontos, mesmo que ponto1 e ponto2 não pertençam a imagem.
    """
    img = bgr.copy()
    lm = LinearRegression()
    #lm = TheilSenRegressor()
    lm = RANSACRegressor(LinearRegression())
    try:
        lm.fit(y_array.reshape(-1,1), x_array.flatten())
        lm = lm.estimator_
    except:
        lm = LinearRegression()
        lm.fit(y_array.reshape(-1,1), x_array.flatten())   
    
    y_img_0 = img.shape[0]/4
    y_img_1 = img.shape[0]
    yr = np.array([y_img_0, y_img_1]).reshape(-1,1)
    xr = lm.predict(yr)
    cv2.line(img, (int(xr[0]), int(yr[0,0])), (int(xr[1]), int(yr[1,0])), (255,0,0), thickness=4)

    return img, lm

def calcular_angulo_com_vertical(img, lm):
    """Não mude ou renomeie esta função
        deve receber uma imagem contendo uma reta, além da reggressão linear e determinar o ângulo da reta com a vertical, utilizando o metodo preferir.
    """
    return math.degrees(math.atan(lm.coef_))

if __name__ == "__main__":
    print('Este script não deve ser usado diretamente')