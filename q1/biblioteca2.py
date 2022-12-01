#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math

#import biblioteca

def segmenta_linha_ciano(bgr):
    """Não mude ou renomeie esta função
        deve receber uma imagem e segmentar as faixas brancas
    """
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mini = (160//2, 50, 50)
    maxi = (200//2, 255, 255)
    mask = cv2.inRange(hsv, mini, maxi)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN, np.ones((3,3),dtype=np.uint8))
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE, np.ones((3,3),dtype=np.uint8))
    
    return mask

def estimar_linha_nas_faixas(img, mask):
    """Não mude ou renomeie esta função
        deve receber uma imagem preta e branca e retorna dois pontos que formen APENAS uma linha em cada faixa. Desenhe cada uma dessas linhas na iamgem.
         formato: [[(x1,y1),(x2,y2)], [(x1,y1),(x2,y2)]]
    """

    edges = cv2.Canny(mask,50,100)
    mask[:] = edges[:]
    lines = cv2.HoughLinesP(edges,1,math.radians(1),10,None,40,30)

    if lines is None or len(lines) < 1:
        return None

    len_L2 = -1
    len_L1 = -1
    x1_1, y1_1, x2_1, y2_1 = 0, 0, 0, 0
    x1_2, y1_2, x2_2, y2_2 = 0, 0, 0, 0
    
    for ((x1,y1,x2,y2),) in lines:

        m = (y2-y1)/(x2-x1+1e-5)
        len2 = (y2-y1)**2 + (x2-x1)**2

        if m > 0.1 and len2 > len_L2:
            len_L2 = len2
            x1_2 = x1
            y1_2 = y1
            x2_2 = x2
            y2_2 = y2
        elif m < -0.1 and len2 > len_L1 :
            len_L1 = len2
            x1_1 = x1
            y1_1 = y1
            x2_1 = x2
            y2_1 = y2
        
    if len_L1 > 0:
        cv2.line(img, (int(x1_1), int(y1_1)), (int(x2_1), int(y2_1)),(0,0,255),5)
        
    if len_L2 > 0:
        cv2.line(img, (int(x1_2), int(y1_2)), (int(x2_2), int(y2_2)),(0,0,255),5)

    
    return [[(x1_1, y1_1),(x2_1, y2_1)],[(x1_2, y1_2),(x2_2, y2_2)]] if len_L1>0 and len_L2>0 else None


def calcular_equacao_das_retas(linhas):
    """Não mude ou renomeie esta função
        deve receber dois pontos que estejam em cada uma das faixas e retornar a equacao das duas retas. Onde y = h + m * x. Formato: [(m1,h1), (m2,h2)]
    """

    (linha_1, linha_2) = linhas
    ((x1_1, y1_1),(x2_1, y2_1)) = linha_1
    ((x1_2, y1_2),(x2_2, y2_2)) = linha_2

    m1 = (y2_1 - y1_1)/(x2_1 - x1_1 + 1e-5)
    h1 = y1_1 - m1 * x1_1

    m2 = (y2_2 - y1_2)/(x2_2 - x1_2 + 1e-5)
    h2 = y1_2 - m2 * x1_2

    if np.isinf((m1, m2)).any() or np.isnan((m1,m2,h1,h2)).any():
        return None
    else: return [(m1,h1), (m2,h2)]

def calcular_ponto_de_fuga(img, equacoes):
    """Não mude ou renomeie esta função
        deve receber duas equacoes de retas e retornar o ponto de encontro entre elas. Desenhe esse ponto na imagem.
    """

    ((m1,h1), (m2,h2)) = equacoes

    xf1 = (h2-h1)/(m1-m2+1e-5)
    yf1 = m1*xf1 + h1

    if np.isinf((xf1, yf1)).any() or np.isnan((xf1,yf1)).any():
        return None
    
    if img is not None:
        try:
            cv2.circle(img,(int(xf1),int(yf1)),5,(0,255,255),-1)
        except:
            return None

    return img, (xf1,yf1)


if __name__ == "__main__":
    linhas = [[(3,2.5),(4,0.6)],[(1,2.4),(0.6,1.1)]]
    equa = calcular_equacao_das_retas(linhas)
    print(equa)
    _, pontof = calcular_ponto_de_fuga(None, equa)
    print(pontof)