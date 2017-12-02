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

# Iniciando o segundo R
def loading2Red():
    print('Loading Red in Green Machine...')

    global state
    global newEvent

    sendMovement(1)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = waitingRed2Machines
            break


# Iniciando o segundo G
def loading2Green():
    print('Loading Green in Red Machine...')

    global state
    global newEvent

    sendMovement(0)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = waitingGreen2Machines
            break


# Esperando finalizar G em qualquer uma das maquinas
def waitingGreen2Machines():
    print('Waiting finish Green | Two machines busy ')

    global state
    global newEvent

    while True:
        if newEvent == 'greenDone':
            newEvent = 'none'
            state = unloadingGreenGreenMachine
            break

# Esperando finalizar G em qualquer uma das maquinas
def waitingRed2Machines():
    print('Waiting finish Red | Two machines busy ')

    global state
    global newEvent

    while True:
        if newEvent == 'redDone':
            newEvent = 'none'
            state = unloadingRedRedMachine
            break

# Finalizando G na maquina Verde
def unloadingGreenGreenMachine():
    print('Unloading Green from Green machine | The Red machine are busy with a Green piece')

    global state
    global newEvent

    sendMovement(3)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = greenFreeRedBusyG
            break

# Finalizando G na maquina Vermelha
def unloadingGreenRedMachine():
    print('Unloading Green from Red machine | The Green machine are busy with a Red piece')

    global state
    global newEvent

    sendMovement(2)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = redFreeGreenBusyR
            break

# Maquina G livre e maquina R ocupada com uma peça verde
def greenFreeRedBusyG():
    print('The Green machine are free | The Red machine are busy with a Green piece')

    global state
    global newEvent

    while True:
        if newEvent == 'greenDone':
            newEvent = 'none'
            state = unloadingGreenOnRed
            break
        elif newEvent == 'redNew':
            newEvent = 'none'
            state = loadingRedInvertOrder

# Finalizando R na maquina vermelha
def unloadingRedRedMachine():
    print('Unloading Red from Red machine | The Green machine are busy with a Red piece')

    global state
    global newEvent

    sendMovement(2)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = redFreeGreenBusyR
            break

# Finalizando R na maquina verde
def unloadingRedGreenMachine():
    print('Unloading Red from Green machine | The Red machine are busy with a Green piece')

    global state
    global newEvent

    sendMovement(3)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = greenFreeRedBusyG
            break

# Maquina R livre e maquina G ocupada com uma peça Vermelha
def redFreeGreenBusyR():

    global state
    global newEvent
    
    print('The Red machine are free | The Green machine are busy with a Red piece')
    while True:
        if newEvent == 'redDone':
            newEvent = 'none'
            state = unloadingRedOnGreen
            break
        elif newEvent == 'greenNew':
            newEvent = 'none'
            state = loadingGreenInvertOrder

# Iniciando G enquanto sua maquina está ocupada
def loadingGreenInvertOrder():
    print('Loading Green... | Green machine busy')

    global state
    global newEvent

    sendMovement(0)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = waitingBusyInvertOrder
            break

# Iniciando R enquanto sua maquina está ocupada
def loadingRedInvertOrder():
    print('Loading Red... | Red machine busy')

    global state
    global newEvent

    sendMovement(1)

    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = waitingBusyInvertOrder
            break

# Esperando a finalização de uma peça quando as ordens estão invertidas
def waitingBusyInvertOrder():
    print('Green machine busy with a Red piece | Red machine busy with a Green piece')

    global state
    global newEvent


    while True:
        if newEvent == 'redDone':
            newEvent = 'none'
            state = unloadingRedGreenMachine
            break
        if newEvent == 'greenDone':
            newEvent = 'none'
            state = unloadingGreenRedMachine
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
        elif newEvent == 'redNew':
            newEvent = 'none'
            state = loading2Red
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
        elif newEvent == 'greenNew':
            newEvent = 'none'
            state = loading2Green
            break

# Iniciando R e esperando finalizar G
def loadingRedWatingGreen():
    print('Loading Red')
    
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
    print('Loading Green')
    
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


# Esperando finalizar um dos dois R
def waiting2Red():
    print('Waiting finish Green')

    global state
    global newEvent

    while True:
        if newEvent == 'redDone':
            newEvent = 'none'
            state = waitingRed
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

#Buscando peça no processo "G" para colocar no buffer de saída;
def unloadingRedOnGreen():
    print('Unloading Red on Green Machine...')

    global state
    global newEvent

    sendMovement(3)
    
    while True:
        if newEvent == 'cytonIdle':
            newEvent = 'none'
            state = idle
            break

#Buscando peça no processo "R" para colocar no buffer de saída;
def unloadingGreenOnRed():
    print('Unloading Green on Red Machine...')

    global state
    global newEvent

    sendMovement(2)
    
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