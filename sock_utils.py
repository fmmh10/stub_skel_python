#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - sock_utils.py
Grupo: 28
Números de aluno: 49990, 50037, 50039
"""

# Zona para fazer imports
import socket as s, sys, struct, pickle

# Programa principal

def create_tcp_server_socket(address, port, queue_size):

	sock = s.socket(s.AF_INET, s.SOCK_STREAM)
	sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
	sock.bind((address, port))
	sock.listen(queue_size)
	return sock

def create_tcp_client_socket(address, port):
	sock = s.socket(s.AF_INET, s.SOCK_STREAM)
	sock.connect((address, port))
	return sock

def receive_all(socket, length):
	msg_recebida = ''

	while(len(msg_recebida) < length):
		msg = socket.recv(length - len(msg_recebida))
		msg_recebida = msg_recebida + msg

	return msg_recebida


def send_data(data, socket):
	msg_bytes = pickle.dumps(data, -1)
	size_bytes = struct.pack('!i', len(msg_bytes))
	socket.sendall(size_bytes)
	socket.sendall(msg_bytes)

def recv_data(socket):
	size_bytes = socket.recv(4)
	size = struct.unpack('!i', size_bytes)[0]
	msg_bytes = receive_all(socket, size)
	return pickle.loads(msg_bytes)
