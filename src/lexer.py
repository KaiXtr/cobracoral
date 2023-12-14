# -*- coding: utf-8 -*-
from posicao import *
from tokens import *
from keywords_PT import *

#######################################
# LEXER
#######################################

class Lexer:
	def __init__(self, fn, texto):
		self.fn = fn
		self.texto = texto
		self.pos = Posicao(-1, 0, -1, fn, texto)
		self.car_atual = None
		self.avancar()
	
	def avancar(self):
		self.pos.avancar(self.car_atual)
		self.car_atual = self.texto[self.pos.idx] if self.pos.idx < len(self.texto) else None

	def criar_tokens(self):
		tokens = []

		while self.car_atual != None:
			#FORMATAÇÃO DE TEXTO E CRIAÇÂO DE VARIÁVEIS
			if self.car_atual in ' \t': self.avancar()
			elif self.car_atual in '#': self.comentario()
			elif self.car_atual in ';\n': tokens.append(Token(TT_NOVALINHA,inicio=self.pos)); self.avancar()
			elif self.car_atual in DIGITOS: tokens.append(self.fazer_num())
			elif self.car_atual in ALFABETO: tokens.append(self.fazer_identificador())
			elif self.car_atual in '"\'': tokens.append(self.fazer_texto())
			elif self.car_atual in ',': tokens.append(Token(TT_VIRGULA,inicio=self.pos)); self.avancar()
			
			#OPERAÇÕES ARITMÉTICAS
			elif self.car_atual in '+∪': tokens.append(self.fazer_op_ou_num('+'))
			elif self.car_atual == '-': tokens.append(self.fazer_op_ou_num('-'))
			elif self.car_atual in '*×': tokens.append(self.fazer_a_ou_b(TT_MUL,TT_POT,'*×'))
			elif self.car_atual in '/\÷': tokens.append(self.fazer_a_ou_b(TT_DIV,TT_RAD,'/\÷'))
			elif self.car_atual in '%': tokens.append(Token(TT_RES,inicio=self.pos)); self.avancar()
			elif self.car_atual in '^': tokens.append(Token(TT_POT,inicio=self.pos)); self.avancar()
			elif self.car_atual in '√': tokens.append(Token(TT_RAD,inicio=self.pos)); self.avancar()
			elif self.car_atual in 'π': tokens.append(Token(TT_PI,inicio=self.pos)); self.avancar()
			
			#COMPARAÇÕES NUMÉRICAS E LÓGICAS
			elif self.car_atual in '=': tokens.append(self.fazer_a_ou_b(TT_IGU,TT_EIG,'='))
			elif self.car_atual in '≠': tokens.append(Token(TT_DIF,inicio=self.pos)); self.avancar()
			elif self.car_atual in '~!':
				token, erro = self.fazer_a_ou_b(None,TT_DIF,'=&|')
				if erro: return [], erro
				else: tokens.append(token)
			elif self.car_atual in '>': tokens.append(self.fazer_a_ou_b(TT_MIQ,TT_MIQIGU,'='))
			elif self.car_atual in '<': tokens.append(self.fazer_a_ou_b(TT_MNQ,TT_MNQIGU,'='))
			elif self.car_atual in '&': tokens.append(Token(TT_PALAVRASCHAVE,'E',inicio=self.pos)); self.avancar()
			elif self.car_atual in '|': tokens.append(Token(TT_PALAVRASCHAVE,'OU',inicio=self.pos)); self.avancar()

			#OPERAÇÕES COM CONJUNTOS
			elif self.car_atual in '∩': tokens.append(Token(TT_INTCONJ,inicio=self.pos)); self.avancar()
			elif self.car_atual in '∈': tokens.append(Token(TT_DENCONJ,inicio=self.pos)); self.avancar()
			elif self.car_atual in '∉': tokens.append(Token(TT_FORCONJ,inicio=self.pos)); self.avancar()
			
			#PARÊNTESES E COLCHETES
			elif self.car_atual == '(': tokens.append(Token(TT_ABRPARENT,inicio=self.pos)); self.avancar()
			elif self.car_atual == ')': tokens.append(Token(TT_FECPARENT,inicio=self.pos)); self.avancar()
			elif self.car_atual == '[': tokens.append(Token(TT_ABRCOLCHE,inicio=self.pos)); self.avancar()
			elif self.car_atual == ']': tokens.append(Token(TT_FECCOLCHE,inicio=self.pos)); self.avancar()
			elif self.car_atual == '{': tokens.append(self.fazer_identificador('ENTÃO')); self.avancar()
			elif self.car_atual == '}': tokens.append(self.fazer_identificador('FIM')); self.avancar()
			
			else:
				inicio = self.pos.copia()
				car = self.car_atual
				self.avancar()
				return [], ErroDeCaractereIlegal(inicio, self.pos, f"'{car}'")
		
		tokens.append(Token(TT_FIM,inicio=self.pos))
		return tokens, None

	def fazer_num(self,num_str=''):
		cont_pont = 0
		inicio = self.pos.copia()

		while self.car_atual != None and self.car_atual in DIGITOS + '.':
			if self.car_atual == '.':
				if cont_pont == 1: break
				cont_pont += 1
			num_str += self.car_atual
			self.avancar()

		if cont_pont == 0: return Token(TT_INTEIRO, int(num_str), inicio, self.pos)
		else: return Token(TT_REAL, float(num_str), inicio, self.pos)

	def fazer_texto(self):
		texto = ''
		inicio = self.pos.copia()
		resultado_de_escape = False
		self.avancar()
		caracteres_de_escape = {'n': '\n','t': '\t'}

		while self.car_atual != None and (self.car_atual != '"' or resultado_de_escape):
			if resultado_de_escape: texto += caracteres_de_escape.get(self.car_atual, self.car_atual)
			else:
				if self.car_atual == '\\': resultado_de_escape = True
				else: texto += self.car_atual
			self.avancar()
			resultado_de_escape = False

		self.avancar()
		return Token(TT_TEXTO, texto, inicio, self.pos)
	
	def fazer_identificador(self,id_str=''):
		inicio = self.pos.copia()

		while self.car_atual != None and self.car_atual in ALFANUMERICO + '_':
			id_str += self.car_atual
			self.avancar()

		if id_str.upper() in TT_OPERAÇÕES.keys(): return Token(TT_OPERAÇÕES[id_str.upper()], inicio=self.pos)
		else: return Token(TT_PALAVRASCHAVE if id_str.upper() in TT_PALAVRASCHAVE else TT_IDE, id_str.upper(), inicio, self.pos)
	
	def fazer_op_ou_num(self,simbolo):
		tok_tipo = simbolo
		inicio = self.pos.copia()
		self.avancar()

		while self.car_atual != None and self.car_atual in ALFANUMERICO + '_':
			if self.car_atual in DIGITOS: tok_tipo = 'NUM'; break
			if self.car_atual in ALFABETO: tok_tipo = 'IDE'; break
			self.avancar()

		if tok_tipo == 'NUM': return self.fazer_num(simbolo)
		elif tok_tipo == 'IDE': return self.fazer_identificador(simbolo)
		else: return Token(TT_MAI if tok_tipo == '+' else TT_MEN, inicio=inicio)
	
	def fazer_a_ou_b(self,a,b,simbolos):
		tok_tipo = a
		inicio = self.pos.copia()
		self.avancar()

		if self.car_atual and self.car_atual in simbolos:
			if simbolos == '~!':
				if self.car_atual == '=': tok_tipo = TT_DIF
				elif self.car_atual == '&': tok_tipo = 'NE'
				elif self.car_atual == '|': tok_tipo = 'NOU'
				else: tok_tipo = b
			else: tok_tipo = b
			self.avancar()

		if a and b: return Token(tok_tipo, inicio=inicio, fim=self.pos)
		elif tok_tipo in TT_PALAVRASCHAVE: return self.fazer_identificador(tok_tipo), None
		elif tok_tipo: return Token(tok_tipo, inicio=inicio, fim=self.pos), None
		else: self.avancar(); return None, ErroDeCaractereEsperado(inicio, self.pos, f"'{simbolos}' ({EM_AFTER} '{tok_tipo}')")

	def comentario(self):
		self.avancar()
		while self.car_atual != '\n' and self.pos.idx < len(self.texto): self.avancar()
		self.avancar()
