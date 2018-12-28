#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 28
Números de aluno: 49990, 50057, 50039
"""

# Zona para fazer imports
import sys
from sock_utils import *
from lock_skel import lock_skel
import select as sel

# Programa principal

if __name__ == "__main__":
    try:
        PORT = int(sys.argv[1])
        n = int(sys.argv[2])
        k = int(sys.argv[3])
        y = int(sys.argv[4])
        t = int(sys.argv[5])
        if n > 0 and t > 0:
            lock_skel = lock_skel(n, k, y, t)
            sock_listen = create_tcp_server_socket("", PORT, 5)     # listen(5)
            SocketList = [sock_listen]

            while True:

                try:
                    R, W, X = sel.select(SocketList, [], [])

                    for sock in R:
                        if sock is sock_listen:
                            (conn_sock, addr) = sock_listen.accept()
                            addr, port = conn_sock.getpeername()

                            print "Connection Accepted!"
                            print "Client: " + addr[0] #FIX: estava só addr e o address está em addr[0] visto que addr contém dois números
                            print "Port: " + str(PORT) #FIX: antes estava como um número e não se pode somar a uma string, dava erro
                            SocketList.append(conn_sock)

                        else:
                            try:
                                lock_skel.clear_expired_locks()       #verifica os recursos com bloqueios que ja tenham expirado o tempo, e desbloqueia os recursos
                                lock_skel.disable()                   #verifica se os recursos já foram bloqueados até ao maximo de vezes, e caso tenham sido, serão inativos
                                mensagem = recv_data(sock)

                                if mensagem:
                                    resposta = lock_skel.processMessage(mensagem)
                                    send_data(resposta,sock)
                                    print lock_skel.lock_pool

                                else:
                                    sock.close()
                                    SocketList.remove(sock)
                                    print "Client connection closed"

                            except:
                                sock.close()
                                SocketList.remove(sock)
                                print "Client connection closed"
                except:
                    print "connection failed"

        else:
            print "INVALID ARGS"
            print "Usage: python lock_server.py <port> <number of resources> <number of allowed blocks for every resource> <number of allowed blocks in an instant> <time of blocks> "


    except IndexError:
        print "MISSING ARGS"

    except ValueError:
        print "INVALID ARGS"
