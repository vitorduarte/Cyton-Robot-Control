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

# Exemplo de estado inicial
def init():
	# Indica novo estado no log para debug
	print('init')
	# As variáveis gobais devem sempre ser chamadas na definição do estado
	global state
	global newEvent

	# Manda pose 0 para o Cyton
	sendMovement(0)

	# Loop que espera o próximo evento
	while True:
		# Condição para cada evento que afeta o estado
		if newEvent == 'cytonIdle':
			# Zerar evento
			newEvent = 'none'
			# Atualizar próximo estado
			state = state0
			# Sair do loop
			break

def state0():
	print('state0')

	global state
	global newEvent

	while True:
		if newEvent == 'loadGreen':
			newEvent = 'none'
			state = state1
			break
		elif newEvent == 'loadRed':
			newEvent = 'none'
			state = state2
			break
	
def state1():
	print('state1')
	global state
	global newEvent

	sendMovement(2)

	while True:
		if newEvent == 'cytonIdle':
			newEvent = 'none'
			state = state0
			break

def state2():
	print('state2')
	global state
	global newEvent

	sendMovement(3)

	while True:
		if newEvent == 'cytonIdle':
			newEvent = 'none'
			state = state0
			break

###################################################
### DECLARAÇÃO DE VARIÁVEIS GLOBAIS - NÃO MEXER! ###
###################################################


state = init
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