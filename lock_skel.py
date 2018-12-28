#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_skel.py
Grupo: 28
Números de aluno: 49990, 50057, 50039
"""

# Zona para fazer imports
from lock_pool import lock_pool

# Programa principal
class lock_skel:	

	def __init__(self, N, K, Y, T):
		self.lock_pool = lock_pool(N, K, Y, T)
		self.N = N		
		self.K = K
		self.Y = Y
		self.T = T

	def processMessage(self, pedido):
		"""Enviado pelo cliente, o pedido é uma lista"""

		resposta = []

		if pedido[0] == 10:
			#LOCK
			resposta.append(11)
			if pedido[2] < self.N and pedido[2] >= 0:
				resposta.append(self.lock_pool.lock(pedido[2], pedido[1], self.T))
				#faz o append de True ou False
			else:
				resposta.append(None)

		elif pedido[0] == 20:
			#RELEASE
			resposta.append(21)
			if pedido[2] < self.N and pedido[2] >= 0:
				#faz o append de True ou False
				resposta.append(self.lock_pool.release(pedido[2], pedido[1]))
			else:
				resposta.append(None)

		elif pedido[0] == 30:
			#TEST
			resposta.append(31)
			if pedido[1] < self.N and pedido[1] >= 0:
				#faz o append de True ou False
				resposta.append(self.lock_pool.test(pedido[1]))
			else:
				resposta.append(None)

		elif pedido[0] == 40:
			#STATS
			resposta.append(41)
			if pedido[1] < self.N and pedido[1] >= 0:
				#faz o append de True ou False
				resposta.append(self.lock_pool.stat(pedido[1]))
			else:
				resposta.append(None)

		elif pedido[0] == 50:
			#STATS-Y
			resposta.append(51)
			resposta.append(self.lock_pool.stat_y())


		elif pedido[0] == 60:
			#STATS-N
			resposta.append(61)
			resposta.append(self.lock_pool.stat_n())

		return resposta
		#envio da resposta depois de processar a mensagem

	def clear_expired_locks(self):
		self.lock_pool.clear_expired_locks()

	def disable(self):
		self.lock_pool.disable()
