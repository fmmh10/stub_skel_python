#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_stub.py
Grupo: 28
Números de aluno: 49990, 50057, 50039
"""
# Zona para fazer imports
from net_client import server

# Programa principal
class lock_stub:
	def __init__(self):
		self.server = None

	def connect(self, host, port):
		self.server = server(host, port)
		self.server.connect()

	def disconnect(self):
		self.server.close()

	def lock(self, client_id, resource_id):
		mensagem = [10, client_id, resource_id]
		resp = self.server.send_receive(mensagem)
		return resp

	def release(self, client_id, resource_id):
		mensagem = [20, client_id, resource_id]
		resp = self.server.send_receive(mensagem)
		return resp

	def test(self, resource_id):
		mensagem = [30, resource_id]
		resp = self.server.send_receive(mensagem)
		return resp

	def stats(self, resource_id):
		mensagem = [40, resource_id]
		resp = self.server.send_receive(mensagem)
		return resp

	def stats_y(self):
		mensagem = [50]
		resp = self.server.send_receive(mensagem)
		return resp

	def stats_n(self):
		mensagem = [60]
		resp = self.server.send_receive(mensagem)
		return resp
