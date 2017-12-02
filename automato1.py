#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AUTOMATO DE EVENTOS NÃO CONTROLÁVEIS

import rospy
from std_msgs.msg import Int8
from std_msgs.msg import String



#######################################
### FUNÇÕES DE CALLBACK - NÃO MEXER ###
#######################################

# Callback para novo evento
def eventCallback(data):
    print('eventCallback')
    global newEvent

    newEvent = data.data


# Função que manda índice de movimento para o Cyton
def sendMovement(move):
    print('sendMovement')
    print(move)
    global pub
    moveToSend = Int8()
    moveToSend = move
    pub.publish(moveToSend)


###########################################
### LISTA DE ESTADOS - EDITE ESTA PARTE ###
###########################################

# Estado inicial em que o robô não está ativo
def idle():
    # Indica novo estado no log para debug
    print('Idle')
    # As variáveis gobais devem sempre ser chamadas na definição do estado
    global state
    global newEvent

    # Loop que espera o próximo evento
    while True:
        # Se tem uma nova peça vermelha
        if newEvent == 'redNew':
            newEvent = 'none'
            state = loadingRed
            break

        # Se tem uma nova peça verde
        elif newEvent == 'greenNew':
            newEvent = 'none'
            state = loadingGreen
            break


# Iniciando R
def loadingRed():
    print('Loading Red...')

    global state
    global newEvent

    sendMovement(0)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = waitingRed
            break

# Iniciando G
def loadingGreen():
    print('Loading Green...')

    global state
    global newEvent

    sendMovement(1)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = waitingGreen
            break

# Esperando finalizar R
def waitingRed():
    print('Waiting finish Red')

    global state
    global newEvent

    while True:
        if newEvent == 'redDone':
            newEvent = 'none'
            state = unloadingRed
            break
        elif newEvent == 'greenNew':
            newEvent = 'none'
            state = loadingGreenWatingRed
            break

# Esperando finalizar G
def waitingGreen():
    print('Waiting finish Green')

    global state
    global newEvent

    while True:
        if newEvent == 'greenDone':
            newEvent = 'none'
            state = unloadingGreen
            break
        elif newEvent == 'redNew':
            newEvent = 'none'
            state = loadingRedWatingGreen
            break

# Iniciando R e esperando finalizar G
def loadingRedWatingGreen():
    print('Loading Red and Wating Green')
    
    global state
    global newEvent

    sendMovement(0)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = waitingRedGreen
            break

# Iniciando G e esperando finalizar R
def loadingGreenWatingRed():
    print('Loading Green and Wating Red')
    
    global state
    global newEvent

    sendMovement(1)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = waitingRedGreen
            break


# Esperando finalizar R ou G
def waitingRedGreen():
    print('Waiting finish Red or Green')

    global state
    global newEvent

    while True:
        if newEvent == 'redDone':
            newEvent = 'none'
            state = unloadingRedWaitingGreen
            break    
        if newEvent == 'greenDone':
            newEvent = 'none'
            state = unloadingGreenWaitingRed
            break

# Finalizando R e esperando finalizar G
def unloadingRedWaitingGreen():
    print('Unloading Red...')

    global state
    global newEvent

    sendMovement(2)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = waitingGreen
            break

# Finalizando G e esperando finalizar R
def unloadingGreenWaitingRed():
    print('Unloading Green...')

    global state
    global newEvent

    sendMovement(3)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = waitingRed
            break

#Buscando peça no processo "R" para colocar no buffer de saída;
def unloadingRed():
    print('Unloading Red...')

    global state
    global newEvent

    sendMovement(2)
    
    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = idle
            break

#Buscando peça no processo "G" para colocar no buffer de saída;
def unloadingGreen():
    print('Unloading Green...')

    global state
    global newEvent

    sendMovement(3)
    
    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = idle
            break

###################################################
### DECLARAÇÃO DE VARIÁVEIS GLOBAIS - NÃO MEXER! ###
###################################################


state = idle
newEvent = 'none'


##############################
### LOOP MAIN - NÃO MEXER! ###
##############################

def main():
    global state
    global pub

    rospy.init_node('automato', anonymous=False)
    pub = rospy.Publisher('move', Int8, queue_size = 10)
    rospy.Subscriber('event', String, eventCallback)

    rospy.sleep(1)

    while not rospy.is_shutdown():
        state()



if __name__ == '__main__':
    main()