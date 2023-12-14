# -*- coding: utf-8 -*-
from keywords_PT import *
from nodes import *
from erros import *

#######################################
# PARSER
#######################################

class ResultadoDoParser:
	def __init__(self):
		self.erro = None
		self.node = None
		self.ultimo_registro_avanco = 0
		self.contagem_de_avancos = 0
		self.reverter_contagem = 0
		
	def registrar_avanco(self):
		self.ultimo_registro_avanco += 1
		self.contagem_de_avancos += 1
		
	def registro(self,resultado):
		self.ultimo_registro_avanco = resultado.contagem_de_avancos
		self.contagem_de_avancos += resultado.contagem_de_avancos
		if resultado.erro: self.erro = resultado.erro
		return resultado.node
		
	def tentar_registrar(self,resultado):
		if resultado.erro:
			self.reverter_contagem = self.contagem_de_avancos
			return None
		return self.registro(resultado)
	
	def sucesso(self,node):
		self.node = node
		return self
	
	def falha(self,erro):
		if not self.erro or self.ultimo_registro_avanco == 0:
			self.erro = erro
		return self

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.ind_tok = -1
		self.avancar()

	def avancar(self):
		self.ind_tok += 1
		self.atualizar_token_atual()
		return self.tok_atual

	def reverso(self, quantidade=1):
		self.ind_tok -= quantidade
		self.atualizar_token_atual()
		return self.tok_atual

	def atualizar_token_atual(self):
		if self.ind_tok >= 0 and self.ind_tok < len(self.tokens):
			self.tok_atual = self.tokens[self.ind_tok]

	def parse(self):
		resultado = self.statements()
		if not resultado.erro and self.tok_atual.tipo != TT_FIM:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Token))
		return resultado

	def statements(self):
		resultado = ResultadoDoParser()
		statements = []
		inicio = self.tok_atual.inicio.copia()

		while self.tok_atual.tipo == TT_NOVALINHA:
			resultado.registrar_avanco()
			self.avancar()

		statement = resultado.registro(self.statement())
		if resultado.erro: return resultado
		statements.append(statement)

		more_statements = True

		while True:
			novalinha_contagem = 0
			while self.tok_atual.tipo == TT_NOVALINHA:
				resultado.registrar_avanco()
				self.avancar()
				novalinha_contagem += 1
			if novalinha_contagem == 0:
				more_statements = False
			
			if not more_statements: break
			statement = resultado.tentar_registrar(self.statement())
			if not statement:
				self.reverso(resultado.reverter_contagem)
				more_statements = False
				continue
			statements.append(statement)

		return resultado.sucesso(NodeLista(statements,inicio,self.tok_atual.fim.copia()))

	def statement(self):
		resultado = ResultadoDoParser()
		inicio = self.tok_atual.inicio.copia()

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_RETORNAR):
			resultado.registrar_avanco()
			self.avancar()

			expr = resultado.tentar_registrar(self.expr())
			if not expr: self.reverso(resultado.reverter_contagem)
			return resultado.sucesso(NodeRetornar(expr, inicio, self.tok_atual.inicio.copia()))
		
		if self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_CONTINUAR):
			resultado.registrar_avanco()
			self.avancar()
			return resultado.sucesso(NodeContinuar(inicio, self.tok_atual.inicio.copia()))
			
		if self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_QUEBRAR):
			resultado.registrar_avanco()
			self.avancar()
			return resultado.sucesso(NodeQuebrar(inicio, self.tok_atual.inicio.copia()))

		expr = resultado.registro(self.expr())
		if resultado.erro:
			return resultado.falha(ErroDeSintaxe(
				self.tok_atual.inicio, self.tok_atual.fim,
				"Esperava 'RETORNAR', 'CONTINUAR', 'QUEBRAR', 'VAR', 'SE', 'PARA', 'ENQUANTO', 'FUNÇÃO', inteiro, real, identificador, '+', '-', '(', '[' ou 'NÃO'"
			))
		return resultado.sucesso(expr)

	def expr(self):
		resultado = ResultadoDoParser()

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_VAR):
			resultado.registrar_avanco()
			self.avancar()

			if self.tok_atual.tipo != TT_IDE:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Identifier))

			nome = self.tok_atual
			resultado.registrar_avanco()
			self.avancar()

			if self.tok_atual.tipo != TT_IGU:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + '='))

			resultado.registrar_avanco()
			self.avancar()
			expr = resultado.registro(self.expr())
			if resultado.erro: return resultado
			return resultado.sucesso(NodeVariavelAssimilar(nome, expr))

		operacoes_logicas = []
		for i in ('E','OU','NE','NOU','XOU','XNOU','=>','<=>'):
			operacoes_logicas.append((TT_PALAVRASCHAVE,i))
			operacoes_logicas.append((TT_PALAVRASCHAVE,i.lower()))
		node = resultado.registro(self.op_bin(self.comp_expr, operacoes_logicas))

		if resultado.erro:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'VAR', 'SE', 'PARA', 'ENQUANTO', 'FUNÇÃO', inteiro, real, identificador, '+', '-', '(', '[' ou 'NÃO'"))

		return resultado.sucesso(node)

	def comp_expr(self):
		resultado = ResultadoDoParser()

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_NAO):
			op_tok = self.tok_atual
			resultado.registrar_avanco()
			self.avancar()

			node = resultado.registro(self.comp_expr())
			if resultado.erro: return resultado
			return resultado.sucesso(NodeOpUni(op_tok, node))
		
		node = resultado.registro(self.op_bin(self.arith_expr, (TT_EIG, TT_DIF, TT_MNQ, TT_MIQ, TT_MNQIGU, TT_MIQIGU)))
		
		if resultado.erro:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "inteiro, real, identificador, '+', '-', '(', '[', 'SE', 'PARA', 'ENQUANTO', 'FUNÇÃO' or 'NÃO'"))
		return resultado.sucesso(node)

	def arith_expr(self):
		return self.op_bin(self.term, (TT_MAI, TT_MEN, TT_DENCONJ,TT_FORCONJ))

	def term(self):
		return self.op_bin(self.factor, (TT_MUL, TT_DIV, TT_RES))

	def pot_e_rad(self):
		return self.op_bin(self.call, (TT_POT, TT_RAD), self.factor)

	def factor(self):
		resultado = ResultadoDoParser()
		tok = self.tok_atual

		if tok.tipo in (TT_MAI, TT_MEN):
			resultado.registrar_avanco()
			self.avancar()
			factor = resultado.registro(self.factor())
			if resultado.erro: return resultado
			return resultado.sucesso(NodeOpBin(tok, factor))

		return self.pot_e_rad()

	def call(self):
		resultado = ResultadoDoParser()
		atom = resultado.registro(self.atom())
		if resultado.erro: return resultado

		if self.tok_atual.tipo == TT_ABRPARENT:
			resultado.registrar_avanco()
			self.avancar()
			nodes_argumentos = []

			if self.tok_atual.tipo == TT_FECPARENT:
				resultado.registrar_avanco()
				self.avancar()
			else:
				nodes_argumentos.append(resultado.registro(self.expr()))
				if resultado.erro:
					return resultado.falha(ErroDeSintaxe(
						self.tok_atual.inicio, self.tok_atual.fim,
						f"{EM_Expected}')', 'VAR', 'SE', 'PARA', 'ENQUANTO', 'FUNÇÃO', inteiro, real, identificador, '+', '-', '(', '[' {EM_Expected} 'NÃO'"
					))

				while self.tok_atual.tipo == TT_VIRGULA:
					resultado.registrar_avanco()
					self.avancar()

					nodes_argumentos.append(resultado.registro(self.expr()))
					if resultado.erro: return resultado

				if self.tok_atual.tipo != TT_FECPARENT:
					return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"{EM_Expected} ',' {EM_OR} ')'"))

				resultado.registrar_avanco()
				self.avancar()
			return resultado.sucesso(NodeChamar(atom, nodes_argumentos))
		return resultado.sucesso(atom)

	def atom(self):
		resultado = ResultadoDoParser()
		tok = self.tok_atual

		if tok.tipo in (TT_INTEIRO, TT_REAL):
			resultado.registrar_avanco()
			self.avancar()
			return resultado.sucesso(NodeNumero(tok))

		elif tok.tipo == TT_TEXTO:
			resultado.registrar_avanco()
			self.avancar()
			return resultado.sucesso(NodeTexto(tok))

		elif tok.tipo == TT_IDE:
			resultado.registrar_avanco()
			self.avancar()
			return resultado.sucesso(NodeVariavelAcesso(tok))

		elif tok.tipo == TT_ABRPARENT:
			resultado.registrar_avanco()
			self.avancar()
			expr = resultado.registro(self.expr())
			if resultado.erro: return resultado
			if self.tok_atual.tipo == TT_FECPARENT:
				resultado.registrar_avanco()
				self.avancar()
				return resultado.sucesso(expr)
			else: return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "')'"))

		elif tok.tipo == TT_ABRCOLCHE:
			list_expr = resultado.registro(self.list_expr())
			if resultado.erro: return resultado
			return resultado.sucesso(list_expr)
		
		elif tok.combinam(TT_PALAVRASCHAVE, PC_SE):
			se_expr = resultado.registro(self.se_expr())
			if resultado.erro: return resultado
			return resultado.sucesso(se_expr)

		elif tok.combinam(TT_PALAVRASCHAVE, PC_PARA):
			para_expr = resultado.registro(self.para_expr())
			if resultado.erro: return resultado
			return resultado.sucesso(para_expr)

		elif tok.combinam(TT_PALAVRASCHAVE, PC_ENQUANTO):
			enquanto_expr = resultado.registro(self.enquanto_expr())
			if resultado.erro: return resultado
			return resultado.sucesso(enquanto_expr)

		elif tok.combinam(TT_PALAVRASCHAVE, PC_FUNCAO):
			func_def = resultado.registro(self.func_def())
			if resultado.erro: return resultado
			return resultado.sucesso(func_def)

		return resultado.falha(ErroDeSintaxe(tok.inicio, tok.fim,EM_Expected + "inteiro, real, identificador, '+', '-', '(', '[', SE', 'PARA', 'ENQUANTO', 'FUNÇÃO'"))

	def list_expr(self):
		resultado = ResultadoDoParser()
		element_nodes = []
		inicio = self.tok_atual.inicio.copia()

		if self.tok_atual.tipo != TT_ABRCOLCHE:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'['"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo == TT_FECCOLCHE:
			resultado.registrar_avanco()
			self.avancar()
		else:
			element_nodes.append(resultado.registro(self.expr()))
			if resultado.erro:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "']', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'"))

			while self.tok_atual.tipo == TT_VIRGULA:
				resultado.registrar_avanco()
				self.avancar()

				element_nodes.append(resultado.registro(self.expr()))
				if resultado.erro: return resultado

			if self.tok_atual.tipo != TT_FECCOLCHE:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"{EM_Expected}',' {EM_OR} ']'"))

			resultado.registrar_avanco()
			self.avancar()

		return resultado.sucesso(NodeLista(element_nodes,inicio,self.tok_atual.fim.copia()))

	def se_expr(self):
		resultado = ResultadoDoParser()
		todos_os_casos = resultado.registro(self.se_expr_casos('SE'))
		if resultado.erro: return resultado
		casos, senao_caso = todos_os_casos
		return resultado.sucesso(NodeSe(casos, senao_caso))

	def se_expr_b(self):
		return self.se_expr_casos('SENÃOSE')
		
	def se_expr_c(self):
		resultado = ResultadoDoParser()
		caso_senao = None

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_SENAO):
			resultado.registrar_avanco()
			self.avancar()

			if self.tok_atual.tipo == TT_NOVALINHA:
				resultado.registrar_avanco()
				self.avancar()

				statements = resultado.registro(self.statements())
				if resultado.erro: return resultado
				caso_senao = (statements, True)

				if self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_FIM):
					resultado.registrar_avanco()
					self.avancar()
				else: return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'FIM'"))
			else:
				expr = resultado.registro(self.statement())
				if resultado.erro: return resultado
				caso_senao = (expr, False)

		return resultado.sucesso(caso_senao)

	def se_expr_b_ou_c(self):
		resultado = ResultadoDoParser()
		casos, caso_senao = [], None

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_SENAOSE):
			todos_os_casos = resultado.registro(self.se_expr_b())
			if resultado.erro: return resultado
			casos, caso_senao = todos_os_casos
		else:
			caso_senao = resultado.registro(self.se_expr_c())
			if resultado.erro: return resultado
		
		return resultado.sucesso((casos, caso_senao))

	def se_expr_casos(self, case_keyword):
		resultado = ResultadoDoParser()
		casos = []
		caso_senao = None

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, case_keyword):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + case_keyword))

		resultado.registrar_avanco()
		self.avancar()

		condicao = resultado.registro(self.expr())
		if resultado.erro: return resultado

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_ENTAO):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'ENTÃO'"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo == TT_NOVALINHA:
			resultado.registrar_avanco()
			self.avancar()

			statements = resultado.registro(self.statements())
			if resultado.erro: return resultado
			casos.append((condicao, statements, True))

			if self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_FIM):
				resultado.registrar_avanco()
				self.avancar()
			else:
				todos_os_casos = resultado.registro(self.se_expr_b_ou_c())
				if resultado.erro: return resultado
				new_cases, caso_senao = todos_os_casos
				casos.extend(new_cases)
		else:
			expr = resultado.registro(self.statement())
			if resultado.erro: return resultado
			casos.append((condicao, expr, False))

			todos_os_casos = resultado.registro(self.se_expr_b_ou_c())
			if resultado.erro: return resultado
			new_cases, caso_senao = todos_os_casos
			casos.extend(new_cases)

		return resultado.sucesso((casos, caso_senao))

	def para_expr(self):
		resultado = ResultadoDoParser()

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_PARA):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'PARA'"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo != TT_IDE:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Identifier))

		nome = self.tok_atual
		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo != TT_IGU:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'='"))
		
		resultado.registrar_avanco()
		self.avancar()

		inicio = resultado.registro(self.expr())
		if resultado.erro: return resultado

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_CADA):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'CADA'"))
		
		resultado.registrar_avanco()
		self.avancar()

		fim = resultado.registro(self.expr())
		if resultado.erro: return resultado

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_PASSO):
			resultado.registrar_avanco()
			self.avancar()

			passo = resultado.registro(self.expr())
			if resultado.erro: return resultado
		else: passo = None

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_ENTAO):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'ENTÃO'"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo == TT_NOVALINHA:
			resultado.registrar_avanco()
			self.avancar()

			body = resultado.registro(self.statements())
			if resultado.erro: return resultado

			if not self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_FIM):
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'FIM'"))

			resultado.registrar_avanco()
			self.avancar()

			return resultado.sucesso(NodePara(nome, inicio, fim, passo, body, True))
		
		body = resultado.registro(self.statement())
		if resultado.erro: return resultado

		return resultado.sucesso(NodePara(nome, inicio, fim, passo, body, False))

	def enquanto_expr(self):
		resultado = ResultadoDoParser()

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_ENQUANTO):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'ENQUANTO'"))

		resultado.registrar_avanco()
		self.avancar()

		condicao = resultado.registro(self.expr())
		if resultado.erro: return resultado

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_ENTAO):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'ENTÃO'"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo == TT_NOVALINHA:
			resultado.registrar_avanco()
			self.avancar()

			corpo = resultado.registro(self.statements())
			if resultado.erro: return resultado

			if not self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_FIM):
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'FIM'"))

			resultado.registrar_avanco()
			self.avancar()

			return resultado.sucesso(NodeEnquanto(condicao, corpo, True))
		
		corpo = resultado.registro(self.statement())
		if resultado.erro: return resultado

		return resultado.sucesso(NodeEnquanto(condicao, corpo, False))

	def func_def(self):
		resultado = ResultadoDoParser()

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_FUNCAO):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'FUNÇÃO'"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.valor in FuncaoInstalada.__dict__.keys():
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_BuiltinFunc))
		elif self.tok_atual.tipo == TT_IDE:
			nome = self.tok_atual
			resultado.registrar_avanco()
			self.avancar()
			if self.tok_atual.tipo != TT_ABRPARENT:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Expected + "'('"))
		else:
			nome = None
			if self.tok_atual.tipo != TT_ABRPARENT:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"{EM_Identifier} {EM_OR} um '('"))
		
		resultado.registrar_avanco()
		self.avancar()
		arg_name_toks = []

		if self.tok_atual.tipo == TT_IDE:
			arg_name_toks.append(self.tok_atual)
			resultado.registrar_avanco()
			self.avancar()
			
			while self.tok_atual.tipo == TT_VIRGULA:
				resultado.registrar_avanco()
				self.avancar()

				if self.tok_atual.tipo != TT_IDE:
					return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,EM_Identifier))

				arg_name_toks.append(self.tok_atual)
				resultado.registrar_avanco()
				self.avancar()
			
			if self.tok_atual.tipo != TT_FECPARENT:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"{EM_Expected}',' {EM_OR} um ')'"))
		else:
			if self.tok_atual.tipo != TT_FECPARENT:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"{EM_Expected} {EM_OR} um ')'"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo == TT_IGU:
			resultado.registrar_avanco()
			self.avancar()

			corpo = resultado.registro(self.expr())
			if resultado.erro: return resultado

			return resultado.sucesso(NodeFuncao(nome,arg_name_toks,corpo,True))
		
		if self.tok_atual.tipo != TT_NOVALINHA:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"{EM_Expected}'=' {EM_OR} NOVALINHA"))

		resultado.registrar_avanco()
		self.avancar()

		corpo = resultado.registro(self.statements())
		if resultado.erro: return resultado

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, PC_FIM):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"{EM_Expected}'FIM'"))

		resultado.registrar_avanco()
		self.avancar()
		
		return resultado.sucesso(NodeFuncao(nome,arg_name_toks,corpo,False))

	def op_bin(self, func_a, ops, func_b=None):
		if func_b == None: func_b = func_a
		
		resultado = ResultadoDoParser()
		esquerdo = resultado.registro(func_a())
		if resultado.erro: return resultado

		while self.tok_atual.tipo in ops or (self.tok_atual.tipo, self.tok_atual.valor) in ops:
			op_tok = self.tok_atual
			resultado.registrar_avanco()
			self.avancar()
			direito = resultado.registro(func_b())
			if resultado.erro: return resultado
			esquerdo = NodeOpBin(esquerdo, op_tok, direito)

		return resultado.sucesso(esquerdo)
