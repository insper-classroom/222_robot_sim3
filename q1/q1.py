#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np
from object_detection_webcam import detect
from biblioteca2 import *
from hough_helper import desenha_circulos

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários
video = "crosshair.mp4"

def calcula_foco():
    h_aviao = 166 # do arquivo
    H_aviao = 3.5 # metros
    D_aviao = 12.65 # metros

    return D_aviao * h_aviao/H_aviao

def laser_acertou(bgr):
    """
    Identifica se o laser acertou o alvo e imprime  resposta na imagem,
    junto com os bounding boxes e imprimir as profundidades no terminal

    Entrada:
    - bgr: imagem original em BGR
    Saída:
    - img: imagem em BGR mostrando as saídas visuais pedidas
    """ 

    img = bgr.copy()
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    # Você deverá trabalhar aqui

    #1. Mostra a distancia focal
    f = calcula_foco()
    print(f"Distância focal: {f}")

    # 2. Detecta o alvo usando a mobilenet
    # O arquivo foi modificado para indicar apenas a detecção de "aeroplane", "car" e "bicycle"
    img, resultados = detect(img)
    cat = None
    H = None
    for resultado in resultados:
        cat, score, (x0,y0), (x1,y1) = resultado
        h = y1 - y0
        if cat == "aeroplane":
            H = 3.5
        elif cat == "car":
            H = 1.8
        elif cat == "bicycle":
            H = 1.0
        break
    
    # 3. Detecta o centro do crossahir pelo ponto de fuga das retas
    pontof = None
    xmedio = None
    mask = segmenta_linha_ciano(bgr)
    cv2.imshow("Mascara", mask)

    result = estimar_linha_nas_faixas(img, mask)
    if result is not None:
        eqs = calcular_equacao_das_retas(result)
        if eqs is not None:
            (m1,h1), (m2,h2) = eqs
            # # Encontra coordenadas de encontro das retas com o fundo da imagem
            # yfundo = 410
            # xfundo1 = (yfundo-h1)/m1
            # xfundo2 = (yfundo-h2)/m2
            # xmedio = (xfundo1+xfundo2)/2

            _, (xfuga, yfuga) = calcular_ponto_de_fuga(img, equacoes=eqs)
    
    # 4. Encontra o centro da circunferência
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=25, minRadius=40, maxRadius=70)
    img = desenha_circulos(img, circles=circles)
    circ = circles[0,0]
    cv2.circle(img, (int(circ[0]), int(circ[1])), radius=3, color=(255,0,255), thickness=-1)

    # 5. Corrigindo o tamanho do alvo pelo seu bounding box
    mask2 = np.zeros_like(gray)
    mask2[gray > 100] = 255
    # Aqui apagamos os pixels pertencentes à máscara do ciano, caso tenha sido detectado
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, np.ones((5,5)))
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, np.ones((5,5)))
    cv2.imshow("Mascara alvo", mask2)
    
    contours, _ = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    max_area = 0
    largest_c = None
    if contours is not None and len(contours) > 0:
        for c in contours:
            area = cv2.contourArea(c)
            if area > max_area:
                max_area = area
                largest_c = c 

    if max_area > 0:
        # Desenha o contorno do retângulo do alvo
        x0, y0, w, h = cv2.boundingRect(largest_c) # atualiza h
        x1, y1 = x0 + w, y0 + h # atualiza x1 e y1
        cv2.drawContours(img, [largest_c], 0, (0,255,255), 5)

    Dist = None
    if H is not None:
        Dist = f * H / h
        print(f"Distância até {cat}: {Dist}")

    # 6. Determina as coordenadas do ponto em que a reta tem a profundidade Dist
    if Dist is not None:
        x_impact = Dist * (xfuga - circ[0])/10 + circ[0]
        y_impact = Dist * (yfuga - circ[1])/10 + circ[1]
        cv2.circle(img,(int(x_impact),int(y_impact)),5,(255,0,255),3)

        # 6. Determina se a reta passou pelo alvo
        xmin, ymin = x0, y0
        xmax, ymax = x1, y1

        # Verifica se o ponto de impacto está dentro do retâncgulo do alvo
        if xmin <= x_impact < xmax and ymin <= y_impact < ymax:
            # Acertou o alvo
            cv2.putText(img, f"ACERTOU {cat}", (50,50),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255),2)

    return img


if __name__ == "__main__":

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture(video)

    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == False:
            #print("Codigo de retorno FALSO - problema para capturar o frame")
            #cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            break

        # Our operations on the frame come here
        img = laser_acertou(frame.copy())

        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('Input', frame)
        cv2.imshow('Output', img)

        # Pressione 'q' para interromper o video
        if cv2.waitKey(1000//30) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

