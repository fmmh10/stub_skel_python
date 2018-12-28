#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_pool.py
Grupo: 28
Números de aluno: 49990, 50057, 50039
"""

# Zona para fazer imports
import sys, time
from sock_utils import *


# Programa principal
class resource_lock:
    def __init__(self):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self.blocked = False
        self.inactive = False
        self.block_count = 0 #quantas vezes já foi bloqueado
        self.client_id = 0   #id do cliente
        self.time_limit = 0  #tempo
        self.start_time = 0


    def lock(self, client_id, time_limit):
        """
        Bloqueia o recurso se este não estiver bloqueado ou inativo, ou mantém o bloqueio
        se o recurso estiver bloqueado pelo cliente client_id. Neste caso renova
        o bloqueio do recurso até time_limit.
        Retorna True se bloqueou o recurso ou False caso contrário.
        """
        resource = False
        if not self.blocked and not self.inactive: # se n estiver bloqueado ou inativo
            self.blocked = True
            self.client_id = client_id
            self.time_limit = time_limit
            self.start_time = time.time()
            self.block_count +=1
            resource = True

        elif self.client_id == client_id and not self.inactive:
            self.time_limit = time_limit
            self.start_time = time.time()
            resource = True

        else:
            resource = False

        return resource



    def urelease(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.blocked = False # desbloqueia o recurso

    def release(self, client_id):
        """
        Liberta o recurso se este foi bloqueado pelo cliente client_id,
        retornando True nesse caso. Caso contrário retorna False.
        """
        resource = False

        if self.client_id == client_id and self.inactive == False: #verifica se é o client_id
            resource = True
            self.blocked = False

        return resource



    def test(self):
        """
        Retorna o estado de bloqueio do recurso ou inativo, caso o recurso se
        encontre inativo.
        """
        state = True
        if self.blocked:
            state = False
        elif self.inactive:
            state = "disable"

        return state

    def stat(self):
        """
        Retorna o número de vezes que este recurso já foi bloqueado em k.
        """
        return self.block_count

    def disable(self):
        """
        Coloca o recurso inativo/indisponível incondicionalmente, alterando os
        valores associados à sua disponibilidade.
        """
        self.blocked = False
        self.inactive = True


        #Perguntar!!!!!!!!!!!!!!!!!!!!!!!

###############################################################################

class lock_pool:
    def __init__(self, N, K, Y, T):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe.
        Define K, o número máximo de bloqueios permitidos para cada recurso. Ao
        atingir K, o recurso fica indisponível/inativo.
        Define Y, o número máximo permitido de recursos bloqueados num dado
        momento. Ao atingir Y, não é possível realizar mais bloqueios até que um
        recurso seja libertado.
		Define T, o tempo máximo de concessão de bloqueio.
        """
        self.lock_list = []
        self.K = K
        self.Y = Y
        self.T = T
        for i in range(N):
            self.lock_list.append(resource_lock())   #adiciona à lista o objeto


    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão do bloqueio. Liberta os recursos caso o seu tempo de
        concessão tenha expirado.
        """
        for recurso in self.lock_list:
            if time.time() - recurso.start_time > recurso.time_limit:
                recurso.urelease()


    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, até ao
        instante time_limit.
        O bloqueio do recurso só é possível se o recurso estiver ativo, não
        bloqueado ou bloqueado para o próprio requerente, e Y ainda não foi
        excedido. É aconselhável implementar um método __try_lock__ para
        verificar estas condições.
        Retorna True em caso de sucesso e False caso contrário.
        """
        resp = False
        if self.stat_y() >= self.Y:
            resp = False
        else:
            resp = self.lock_list[resource_id].lock(client_id, self.T)

        return resp

    def release(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        True em caso de sucesso e False caso contrário.
        """
        return self.lock_list[resource_id].release(client_id)  #liberta o recurso

    def test(self,resource_id):
        """
        Retorna True se o recurso resource_id estiver desbloqueado e False caso
        esteja bloqueado ou inativo.
        """
        return self.lock_list[resource_id].test() #checa o estado do recurso

    def stat(self,resource_id):
        """
        Retorna o número de vezes que o recurso resource_id já foi bloqueado, dos
        K bloqueios permitidos.
        """
        return self.lock_list[resource_id].stat()


    def stat_y(self):
        """
        Retorna o número de recursos bloqueados num dado momento do Y permitidos.
        """
        recursos_bloqueados = 0

        for id_recurso in range(len(self.lock_list)):
            if self.test(id_recurso) == False :
                recursos_bloqueados = recursos_bloqueados + 1
        return recursos_bloqueados

    def stat_n(self):
        """
        Retorna o número de recursos disponíneis em N.
        """
        recursos_disponiveis = 0
        for id_recurso in range(len(self.lock_list)):
            if self.test(id_recurso) == True:
                recursos_disponiveis = recursos_disponiveis + 1
        return recursos_disponiveis

    def disable(self):
        for id_recurso in range(len(self.lock_list)):
            if self.stat(id_recurso) >=  self.K:
                self.lock_list[id_recurso].disable()
            else:
                pass

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print.
        """
        output = ""
        for id_recurso in range(len(self.lock_list)):
            recurso = self.lock_list[id_recurso]
            if self.test(id_recurso) == False:
                output += "recurso " + str(id_recurso) + " bloqueado pelo cliente " + str(recurso.client_id) + " ate " + time.ctime(recurso.start_time + recurso.time_limit) + "\n"
            elif self.test(id_recurso) == "disable":
                output += "recurso " + str(id_recurso) + " inativo\n"
            else:
                output += "recurso " + str(id_recurso) + " desbloqueado\n"


        #
        # Acrescentar na output uma linha por cada recurso bloqueado, da forma:
        # recurso <número do recurso> bloqueado pelo cliente <id do cliente> até
        # <instante limite da concessão do bloqueio>
        #
        # Caso o recurso não esteja bloqueado a linha é simplesmente da forma:
        # recurso <número do recurso> desbloqueado
        # Caso o recurso não esteja inativo a linha é simplesmente da forma:
        # recurso <número do recurso> inativo
        #
        return output
