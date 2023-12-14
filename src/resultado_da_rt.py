# -*- coding: utf-8 -*-
#######################################
# RESULTADO DA EXECUÇÃO (RUNTIME)
#######################################

class ResultadoDaRT:
	def __init__(self):
		self.reiniciar()
		
	def reiniciar(self):
		self.valor = None
		self.erro = None
		self.valor_retornado_da_funcao = None
		self.loop_deve_continuar = False
		self.loop_deve_quebrar = False
		
	def registro(self,resultado):
		self.erro = resultado.erro
		self.valor_retornado_da_funcao = resultado.valor_retornado_da_funcao
		self.loop_deve_continuar = resultado.loop_deve_continuar
		self.loop_deve_quebrar = resultado.loop_deve_quebrar
		return resultado.valor
		
	def sucesso(self,valor):
		self.reiniciar()
		self.valor = valor
		return self
		
	def sucesso_do_retornar(self,valor):
		self.reiniciar()
		self.valor_retornado_da_funcao = valor
		return self
		
	def sucesso_do_continuar(self,valor):
		self.reiniciar()
		self.loop_deve_continuar = valor
		return self
		
	def sucesso_do_quebrar(self,valor):
		self.reiniciar()
		self.loop_deve_quebrar = valor
		return self
		
	def falha(self,erro):
		self.reiniciar()
		self.erro = erro
		return self
		
	def deve_retornar(self):
		return (self.erro or self.valor_retornado_da_funcao or self.loop_deve_continuar or self.loop_deve_quebrar)
