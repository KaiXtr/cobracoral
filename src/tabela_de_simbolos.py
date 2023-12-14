# -*- coding: utf-8 -*-
#######################################
# TABELA DE SÍMBOLOS
#######################################

class TabelaDeSimbolos:
	def __init__(self,pai=None):
		self.simbolos = {}
		self.pai = pai
	
	def obter(self,nome):
		valor = self.simbolos.get(nome,None)
		if valor == None and self.pai:
			return self.pai.obter(nome)
		return valor
		
	def criar(self,nome,valor):
		self.simbolos[nome] = valor
		
	def remover(self,nome):
		del self.simbolos[nome]