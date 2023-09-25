from keywords_PT import *

#######################################
# ERROS
#######################################

class Erro:
	def __init__(self, inicio, fim, nome_do_erro, detalhes):
		self.inicio = inicio
		self.fim = fim
		self.nome_do_erro = nome_do_erro
		self.detalhes = detalhes
	
	def como_texto(self):
		resultado = f'{self.nome_do_erro}: {self.detalhes}\n{EM_FILE} {self.inicio.fn}, {EM_LINE} {self.inicio.ln + 1}'
		return resultado

class ErroDeCaractereIlegal(Erro):
	def __init__(self, inicio, fim, detalhes):
		super().__init__(inicio, fim, EM_IlegalChar, detalhes)

class ErroDeCaractereEsperado(Erro):
	def __init__(self, inicio, fim, detalhes):
		super().__init__(inicio, fim, EM_ExpectedChar, detalhes)

class ErroDeSintaxe(Erro):
	def __init__(self, inicio, fim, detalhes):
		super().__init__(inicio, fim, EM_Sintax, detalhes)

class ErroRT(Erro):
	def __init__(self,inicio,fim,detalhes,contexto):
		super().__init__(inicio, fim, f'\t{EM_Runtime}', detalhes)
		self.contexto = contexto
	
	def como_texto(self):
		resultado = self.gerar_traceback() + f'{self.nome_do_erro}: {self.detalhes}\n'
		return resultado
		
	def gerar_traceback(self):
		resultado = ''
		pos = self.inicio
		ctx = self.contexto
		
		while ctx:
			resultado = f'\t{EM_FILE} {pos.fn}, {EM_LINE} {str(pos.ln + 1)} {EM_IN} {ctx.mostrar_nome}\n' + resultado
			pos = ctx.posicao_do_pai
			ctx = ctx.pai
		
		return EM_Traceback + '\n' + resultado