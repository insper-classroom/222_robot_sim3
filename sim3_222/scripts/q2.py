#! /usr/bin/env python3
# -*- coding:utf-8 -*-


from __future__ import print_function, division
import auxiliar
import rospy
import numpy as np
import math
import cv2
import time
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image, CompressedImage, LaserScan
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist, Vector3, Pose

from nav_msgs.msg import Odometry


bridge = CvBridge()

# Imagem vinda da câmera do robô
cv_image = None
# Ponto de referência usado para o controle do robô
media = []
# Centro da imagem
centro = []


# A função a seguir é chamada sempre que chega um novo frame
def roda_todo_frame(imagem):
    print("frame")
    global cv_image
    global media
    global centro
    
    try:
        cv_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8")
        # - * Processar AQUI sua imagem  * - #
        img = cv_image.copy()

        # ATENÇÃO: ao mostrar a imagem aqui, não podemos usar cv2.imshow() dentro do while principal!! 
        cv2.imshow("Referencia", img)
        cv2.waitKey(1)
    except CvBridgeError as e:
        print('ex', e)



if __name__=="__main__":
    rospy.init_node("Q2")

    topico_imagem = "/camera/image/compressed"

    recebedor = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame, queue_size=4, buff_size = 2**24)
    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
    
    try:
        vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
        
        while not rospy.is_shutdown():
            
            # -- Loop de controle do robô -- #

            velocidade_saida.publish(vel)
            rospy.sleep(0.1)

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")

