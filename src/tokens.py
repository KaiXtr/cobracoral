# -*- coding: utf-8 -*-
#######################################
# TOKENS
#######################################

class Token:
	def __init__(self, tipo, valor=None, inicio=None, fim=None):
		self.tipo = tipo
		self.valor = valor
		if inicio:
			self.inicio = inicio.copia()
			self.fim = inicio.copia()
			self.fim.avancar()
		if fim: self.fim = fim.copia()
	
	def __repr__(self):
		if self.valor: return f'{self.tipo}:{self.valor}'
		return f'{self.tipo}'
		
	def combinam(self,tipo,valor):
		if isinstance(valor,tuple):
			t = False
			for i in valor:
				if t == False: t = self.tipo == tipo and self.valor == i
			return t
		else: return self.tipo == tipo and self.valor == valor
