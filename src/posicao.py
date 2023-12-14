# -*- coding: utf-8 -*-
#######################################
# POSIÇÃO
#######################################

class Posicao:
	def __init__(self, idx, ln, col, fn, ftxt):
		self.idx = idx
		self.ln = ln
		self.col = col
		self.fn = fn
		self.ftxt = ftxt

	def avancar(self, car_atual=None):
		self.idx += 1
		self.col += 1

		if car_atual == '\n':
			self.ln += 1
			self.col = 0

		return self

	def copia(self):
		return Posicao(self.idx, self.ln, self.col, self.fn, self.ftxt)