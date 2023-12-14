# -*- coding: utf-8 -*-
#######################################
# CONTEXTO
#######################################

class Contexto:
	def __init__(self,mostrar_nome=None,pai=None,posicao_do_pai=None):
		self.mostrar_nome = mostrar_nome
		self.pai = pai
		self.posicao_do_pai = posicao_do_pai
		self.tabela_simbolos = None