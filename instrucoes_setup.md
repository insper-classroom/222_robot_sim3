
## Jupyterlab

Para instalar Jupyterlab no Linux faça: 

    pip install jupyterlab



## Gazebo Turtlebot

Certifique-se de que seu `robotica.sh` tem as variáveis `ROS_IP` e `ROS_MASTER_URI` desabilitadas antes e rodar o Gazebo.

Essas variáveis estarão desabilitadas se tiverem um `#` precedendo a linha. 

## Versão do Python

Os códigos ROS são compatíveis somente com Python 3.

Prefira executar as questões de ROS usando o comando `rosrun`.

Caso queira executar a partir do VSCode, certifique-se que o item `Terminal: Execute in File Dir` esteja marcado.

## Teleop

Sempre que usar o  `teleop` encerre o programa logo em seguida.  Enquanto estiver aberto o `teleop` ficará enviando comandos de velocidade para o robô, conflitando com seus programas que controlam o robô. 

Lembrando que para lançar o teleop faça: 

    roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

Feche o `teleop` depois de usar.


## catkin_make

Executar `catkin_make` após fazer o download do projeto: 

    cd ~/catkin_ws/
    catkin_make

## Onde baixar os arquivos

O código deve sempre ser baixado na pasta `cd ~/catkin_make/src` :

    cd ~/catkin_ws/src
    git clone <nome do repo>

## Arquivos executáveis

Certifique-se de que seus scripts Python são executáveis

    roscd p2_221
    cd scripts
    chmod a+x *.py

## Executar prova

Para executar arquivos do ROS, faça:

    rosrun p2_221 arquivo.py 

Onde `arquivo.py` é algum script Python executável que você deve ter na pasta `p2_221/scripts`.


Certifique-se de que seus scripts ROS rodam com Python 3

## Commit no Github

    Lembre-se, de regularmente fazer
        cd ~/catkin_ws/src/PROVA
        git add --all
        git commit -m "Mensagem aqui"
        git push

