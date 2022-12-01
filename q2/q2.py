#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários
video = "pedra-papel-tesoura.mp4"

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
        img = frame.copy()

        # A estratégia que vamos usar é a análise das relações de dimensões e área de um contorno
        # Primeiro separamos os contornos de ambas as mãos (direita e esquerda)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = np.zeros_like(gray)
        mask[gray < 240] = 255
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5)))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5)))
    
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # Assumimos que há apenas dois contornos
        x0, y0, w0, h0 = cv2.boundingRect(contours[0])
        x1, y1, w1, h1 = cv2.boundingRect(contours[1])

        if x0 < x1:
            # Recortamos apenas a metade do contorno correspondente à mão do jogador
            # Mão esquerda
            cv2.rectangle(img, (x0+w0//2,y0),(x0+w0,y0+h0),(0,255,255),3)
            roi_left = mask[y0:y0+h0, x0+w0//2:x0+w0]
            # Mão direita
            cv2.rectangle(img, (x1,y1),(x1+w1//2,y1+h1),(255,255,0),3)
            roi_right = mask[y1:y1+h1, x1:x1+w1//2]

        else:
            # Recortamos apenas a metade do contorno correspondente à mão do jogador
            # Mão esquerda
            cv2.rectangle(img, (x1+w1//2,y1),(x1+w1,y1+h1),(0,255,255),3)
            roi_left = mask[y1:y1+h1, x1+w1//2:x1+w1]
            # Mão direita
            cv2.rectangle(img, (x0,y0),(x0+w0//2,y0+h0),(255,255,0),3)
            roi_right = mask[y0:y0+h0, x0:x0+w0//2]
        

        # Critério para 'pedra': altura da roi maior do que a largura
        if roi_left.shape[0] >= roi_left.shape[1]:
            player_left = 'pedra'
        else:
            # Para distinguir entre papel e tesoura, fazemos a relação entre a área do contorno e a área da ROI
            contours, _ = cv2.findContours(roi_left, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            if cv2.contourArea(contours[0])/(roi_left.shape[0]*roi_left.shape[1]) < 0.65:
                player_left = 'tesoura'
            else:
                player_left = 'papel'

        # Fazemos o mesmo, mas agora para o player da direita
        # Critério para 'pedra': altura da roi maior do que a largura
        if roi_right.shape[0] >= roi_right.shape[1]:
            player_right = 'pedra'
        else:
            # Para distinguir entre papel e tesoura, fazemos a relação entre a área do contorno e a área da ROI
            contours, _ = cv2.findContours(roi_right, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            if cv2.contourArea(contours[0])/(roi_right.shape[0]*roi_right.shape[1]) < 0.65:
                player_right = 'tesoura'
            else:
                player_right = 'papel'

        # Compara as jogadas e decide quem ganhou
        if player_left == player_right:
            decision_left = 'empatou'
            decision_right = 'empatou'
        elif player_left == 'pedra':
            if player_right == 'papel':
                decision_left = 'perdeu'
                decision_right = 'ganhou'
            else:
                decision_left = 'ganhou'
                decision_right = 'perdeu'
        elif player_left == 'papel':
            if player_right == 'tesoura':
                decision_left = 'perdeu'
                decision_right = 'ganhou'
            else:
                decision_left = 'ganhou'
                decision_right = 'perdeu'
        elif player_left == 'tesoura':
            if player_right == 'pedra':
                decision_left = 'perdeu'
                decision_right = 'ganhou'
            else:
                decision_left = 'ganhou'
                decision_right = 'perdeu'

        texto = f"Jogador 1 = {player_left} {decision_left} e Jogador 2 = {player_right} {decision_right}"
        cv2.putText(img, texto, (50,50),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255),1)

        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('Input', frame)
        cv2.imshow('Mask', mask)
        cv2.imshow('Output', img)

        # Pressione 'q' para interromper o video
        if cv2.waitKey(1000//30) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

