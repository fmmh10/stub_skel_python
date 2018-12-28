#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: 28
Números de aluno: 49990, 50057, 50039
"""

# Zona para fazer imports
import sys
from lock_stub import lock_stub

# Programa principal
if __name__ == "__main__":
    try:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
        client_id = int(sys.argv[3])

        stub = lock_stub()
        stub.connect(HOST, PORT)


        while True:
            msg = raw_input("Comando > ")
            if msg == 'sair':
                stub.disconnect()
                break
            try:
                msg = msg.split()

                if msg[0] == "LOCK":
                    response = stub.lock(int(msg[1]), int(msg[2]))
                    #se usar client_id garante que n há falha quando for introduzido um id diferente no comando LOCK

                elif msg[0] == "RELEASE":
                    response = stub.release(int(msg[1]), int(msg[2]))
                    #se usar client_id garante que n há falha quando for introduzido um id diferente no comando LOCK

                elif msg[0] == "TEST":
                    response = stub.test(int(msg[1]))

                elif msg[0] == "STATS":
                    response = stub.stats(int(msg[1]))

                elif msg[0] == "STATS-Y":
                    response = stub.stats_y()

                elif msg[0] == "STATS-N":
                    response = stub.stats_n()

                else:
                    response = "UNKNOW COMMAND"

                print response

            except IndexError:
                print "MISSING ARGUMENTS"
                print "Usage: python lock_client.py <ip> <port> <cliente_id>"

            except ValueError:
                print "INVALID ARGUMENTS"
                print "Usage: python lock_client.py <ip> <port> <cliente_id>"

            except:
                print "Server not available"
                stub.disconnect()
                break

    except:
        print "Server not available"
