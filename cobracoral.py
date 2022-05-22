#######################################
# CONSTANTES
#######################################

import datetime
import string
import time
import os

ALFABETO = 'abcdefghijklmnopqrstuvwxyz'
ACENTOS = 'äåæªáãàçâéèêíìîñóòôõúù'
ALFABETO += ACENTOS + ACENTOS.upper() + ALFABETO.upper()
DIGITOS = '0123456789'
ALFANUMERICO = ALFABETO + DIGITOS

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
		resultado = f'{self.nome_do_erro}: {self.detalhes}\nArquivo {self.inicio.fn}, linha {self.inicio.ln + 1}'
		return resultado

class ErroDeCaractereIlegal(Erro):
	def __init__(self, inicio, fim, detalhes):
		super().__init__(inicio, fim, 'Este caractere não deveria estar aqui!', detalhes)

class ErroDeCaractereEsperado(Erro):
	def __init__(self, inicio, fim, detalhes):
		super().__init__(inicio, fim, 'Eu estava esperando outro caractere...', detalhes)

class ErroDeSintaxe(Erro):
	def __init__(self, inicio, fim, detalhes):
		super().__init__(inicio, fim, 'Esta linha não está bem estruturada!', detalhes)

class ErroRT(Erro):
	def __init__(self,inicio,fim,detalhes,contexto):
		super().__init__(inicio, fim, '\tErro de processamento', detalhes)
		self.contexto = contexto
	
	def como_texto(self):
		resultado = self.gerar_traceback() + f'{self.nome_do_erro}: {self.detalhes}\n'
		return resultado
		
	def gerar_traceback(self):
		resultado = ''
		pos = self.inicio
		ctx = self.contexto
		
		while ctx:
			resultado = f'\tArquivo {pos.fn}, linha {str(pos.ln + 1)} in {ctx.mostrar_nome}\n' + resultado
			pos = ctx.posicao_do_pai
			ctx = ctx.pai
		
		return 'O caminho de volta: (última linha executada por último):\n' + resultado
			
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

#######################################
# TOKENS
#######################################

TT_INTEIRO	= 'INTEIRO'
TT_REAL		 = 'REAL'
TT_LOGICO	 = 'LÓGICO'
TT_TEXTO		= 'TEXTO'
TT_VER		= 'VERDADEIRO'
TT_FAL		= 'FALSO'
TT_IDE		= 'IDENTIFICADOR'
TT_PCH		= 'PALAVRACHAVE'

TT_PONTO		= 'PONTO'
TT_VIRGULA		= 'VÍRGULA'
TT_SETA		 = 'SETA'
TT_NOVALINHA	= 'NOVALINHA'
TT_FIM		= 'FIM'

TT_MAI		= 'ADIÇÃO'
TT_MEN		= 'SUBTRAÇÃO'
TT_MUL		= 'MULTIPLICAÇÃO'
TT_DIV		= 'DIVISÃO'
TT_POT		= 'POTENCIAÇÃO'
TT_RAD		= 'RADICIAÇÃO'
TT_LOG		= 'LOGARITMO'
TT_RES		= 'RESTO'

TT_PI		 = 'VALOR DE PI'

TT_IGU 		= 'IGUAL A'
TT_EIG		= 'É IGUAL A'
TT_DIF		= 'DIFERENTE'
TT_MIQ		= 'MAIOR QUE'
TT_MNQ		= 'MENOR QUE'
TT_MIQIGU	 = 'MAIOR OU IGUAL A'
TT_MNQIGU	 = 'MENOR OU IGUAL A'

TT_ABRPARENT	= 'ABRPARENT'
TT_FECPARENT	= 'FECPARENT'
TT_ABRCOLCHE	= 'ABRCOLCHE'
TT_FECCOLCHE	= 'FECCOLCHE'

TT_PALAVRASCHAVE = [
	'VAR','E','OU','NE','NOU','XOU','XNOU','=>','<=>','NÃO','NAO','SE','SENÃOSE','SENAOSE','SENÃO','SENAO',
	'PARA','CADA','PASSO','ENQUANTO','FUNÇÃO','FUNCÃO','FUNÇAO','FUNCAO',
	'ENTÃO','ENTAO','FIM','RETORNAR','CONTINUAR','QUEBRAR'
]
TT_PALAVRASCHAVE += [i.lower() for i in TT_PALAVRASCHAVE]

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
			if self.car_atual in ' \t': self.avancar()
			elif self.car_atual in '#': self.comentario()
			elif self.car_atual in ';\n': tokens.append(Token(TT_NOVALINHA,inicio=self.pos)); self.avancar()
			elif self.car_atual in DIGITOS: tokens.append(self.fazer_num())
			elif self.car_atual in ALFABETO: tokens.append(self.fazer_identificador())
			elif self.car_atual in '"' + "'": tokens.append(self.fazer_texto())
			elif self.car_atual in ',': tokens.append(Token(TT_VIRGULA,inicio=self.pos)); self.avancar()
			
			elif self.car_atual == '+': tokens.append(Token(TT_MAI,inicio=self.pos)); self.avancar()
			elif self.car_atual == '-': tokens.append(self.fazer_a_ou_b(TT_MEN,TT_SETA,'>'))
			elif self.car_atual in '*×': tokens.append(self.fazer_a_ou_b(TT_MUL,TT_POT,'*×'))
			elif self.car_atual in '/\÷': tokens.append(self.fazer_a_ou_b(TT_DIV,TT_RAD,'/\÷'))
			elif self.car_atual in '%': tokens.append(Token(TT_RES,inicio=self.pos)); self.avancar()
			elif self.car_atual in '^': tokens.append(Token(TT_POT,inicio=self.pos)); self.avancar()
			elif self.car_atual in '√': tokens.append(Token(TT_RAD,inicio=self.pos)); self.avancar()
			
			elif self.car_atual in 'π': tokens.append(Token(TT_PI,inicio=self.pos)); self.avancar()
			
			elif self.car_atual in '=': tokens.append(self.fazer_a_ou_b(TT_IGU,TT_EIG,'='))
			elif self.car_atual in '≠': tokens.append(Token(TT_DIF,inicio=self.pos)); self.avancar()
			elif self.car_atual in '~!':
				token, erro = self.fazer_a_ou_b(None,TT_DIF,'=')
				if erro: return [], erro
				else: tokens.append(token)
			elif self.car_atual in '>': tokens.append(self.fazer_a_ou_b(TT_MIQ,TT_MIQIGU,'='))
			elif self.car_atual in '<': tokens.append(self.fazer_a_ou_b(TT_MNQ,TT_MNQIGU,'='))
			elif self.car_atual in '&': tokens.append(Token(TT_PALAVRASCHAVE,'E',inicio=self.pos)); self.avancar()
			elif self.car_atual in '|': tokens.append(Token(TT_PALAVRASCHAVE,'OU',inicio=self.pos)); self.avancar()
			
			elif self.car_atual == '(': tokens.append(Token(TT_ABRPARENT,inicio=self.pos)); self.avancar()
			elif self.car_atual == ')': tokens.append(Token(TT_FECPARENT,inicio=self.pos)); self.avancar()
			elif self.car_atual == '[': tokens.append(Token(TT_ABRCOLCHE,inicio=self.pos)); self.avancar()
			elif self.car_atual == ']': tokens.append(Token(TT_FECCOLCHE,inicio=self.pos)); self.avancar()
			
			else:
				inicio = self.pos.copia()
				car = self.car_atual
				self.avancar()
				return [], ErroDeCaractereIlegal(inicio, self.pos, "'" + car + "'")
		
		tokens.append(Token(TT_FIM,inicio=self.pos))
		return tokens, None

	def fazer_num(self):
		num_str = ''
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
	
	def fazer_identificador(self):
		id_str = ''
		inicio = self.pos.copia()

		while self.car_atual != None and self.car_atual in ALFANUMERICO + '_':
			id_str += self.car_atual
			self.avancar()

		tok_tipo = TT_PALAVRASCHAVE if id_str in TT_PALAVRASCHAVE else TT_IDE
		return Token(tok_tipo, id_str, inicio, self.pos)

	def fazer_a_ou_b(self,a,b,simbolos):
		tok_tipo = a
		inicio = self.pos.copia()
		self.avancar()

		if self.car_atual in simbolos:
			self.avancar()
			tok_tipo = b

		if a and b: return Token(tok_tipo, inicio=inicio, fim=self.pos)
		elif tok_tipo: return Token(tok_tipo, inicio=inicio, fim=self.pos), None
		else: self.avancar(); return None, ErroDeCaractereEsperado(inicio, self.pos, f"'{simbolos}' (depois de '{a}')")

	def comentario(self):
		self.avancar()
		while self.car_atual != '\n': self.avancar()
		self.avancar()
		
#######################################
# NODES
#######################################

class NodeNumero:
	def __init__(self,token):
		self.token = token
		self.inicio = token.inicio
		self.fim = token.fim
	
	def __repr__(self):
		return self.token
		
class NodeTexto:
	def __init__(self,token):
		self.token = token
		self.inicio = token.inicio
		self.fim = token.fim
	
	def __repr__(self):
		return self.token

class NodeLista:
	def __init__(self,elementos,inicio,fim):
		self.elementos = elementos
		self.inicio = inicio
		self.fim = fim
	
	def __repr__(self):
		return self.elementos

class NodeVariavelAcesso:
	def __init__(self,nome):
		self.nome = nome
		self.inicio = nome.inicio
		self.fim = nome.fim
	
	def __repr__(self):
		return self.nome

class NodeVariavelAssimilar:
	def __init__(self,nome,valor):
		self.nome = nome
		self.valor = valor
		self.inicio = nome.inicio
		self.fim = valor.fim
	
	def __repr__(self):
		return self.nome

class NodeOpUni:
	def __init__(self,tok_op,node):
		self.tok_op = tok_op
		self.node = node
		self.inicio = tok_op.inicio
		self.fim = node.fim
		
	def __repr__(self):
		return f'({self.tok_op},{self.node})'

class NodeOpBin:
	def __init__(self,esquerdo,tok_op,direito):
		self.node_esquerdo = esquerdo
		self.tok_op = tok_op
		self.node_direito = direito
		self.inicio = esquerdo.inicio
		self.fim = direito.fim
		
	def __repr__(self):
		return f'({self.node_esquerdo},{self.tok_op},{self.node_direito})'

class NodeSe:
	def __init__(self, casos, senao):
		self.casos = casos
		self.senao = senao
		self.inicio = self.casos[0][0].inicio
		self.fim = (self.senao or self.casos[len(self.casos) - 1])[0].fim

class NodeEnquanto:
	def __init__(self, node_condicao, node_corpo, retornar_automaticamente):
		self.node_condicao = node_condicao
		self.node_corpo = node_corpo
		self.retornar_automaticamente = retornar_automaticamente
		self.inicio = self.node_condicao.inicio
		self.fim = self.node_corpo.fim

class NodePara:
	def __init__(self, node_nome, node_inicio, node_final, node_passo, node_corpo, retornar_automaticamente):
		self.node_nome = node_nome
		self.node_inicio = node_inicio
		self.node_final = node_final
		self.node_passo = node_passo
		self.node_corpo = node_corpo
		self.retornar_automaticamente = retornar_automaticamente
		self.inicio = self.node_nome.inicio
		self.fim = self.node_corpo.fim

class NodeFuncao:
	def __init__(self, node_nome, tokens_nomes, node_corpo, retornar_automaticamente):
		self.node_nome = node_nome
		self.tokens_nomes = tokens_nomes
		self.node_corpo = node_corpo
		self.retornar_automaticamente = retornar_automaticamente

		if self.node_nome: self.inicio = self.node_nome.inicio
		elif len(self.tokens_nomes) > 0: self.inicio = self.tokens_nomes[0].inicio
		else: self.inicio = self.node_corpo.inicio

		self.fim = self.node_corpo.fim

class NodeChamar:
	def __init__(self, node_chamado, nodes):
		self.node_chamado = node_chamado
		self.nodes = nodes
		self.inicio = self.node_chamado.inicio

		if len(self.nodes) > 0: self.fim = self.nodes[len(self.nodes) - 1].fim
		else: self.fim = self.node_chamado.fim

class NodeRetornar:
	def __init__(self, node, inicio, fim):
		self.node = node
		self.inicio = inicio
		self.fim = fim

class NodeContinuar:
	def __init__(self, inicio, fim):
		self.inicio = inicio
		self.fim = fim

class NodeQuebrar:
	def __init__(self, inicio, fim):
		self.inicio = inicio
		self.fim = fim

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
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,"Token não pode aparecer após tokens anteriores"))
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

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, 'RETORNAR'):
			resultado.registrar_avanco()
			self.avancar()

			expr = resultado.tentar_registrar(self.expr())
			if not expr: self.reverso(resultado.reverter_contagem)
			return resultado.sucesso(NodeRetornar(expr, inicio, self.tok_atual.inicio.copia()))
		
		if self.tok_atual.combinam(TT_PALAVRASCHAVE, 'CONTINUAR'):
			resultado.registrar_avanco()
			self.avancar()
			return resultado.sucesso(NodeContinuar(inicio, self.tok_atual.inicio.copia()))
			
		if self.tok_atual.combinam(TT_PALAVRASCHAVE, 'QUEBRAR'):
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

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, 'VAR'):
			resultado.registrar_avanco()
			self.avancar()

			if self.tok_atual.tipo != TT_IDE:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,"Esperava identificador"))

			nome = self.tok_atual
			resultado.registrar_avanco()
			self.avancar()

			if self.tok_atual.tipo != TT_IGU:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,"Esperava um '='"))

			resultado.registrar_avanco()
			self.avancar()
			expr = resultado.registro(self.expr())
			if resultado.erro: return resultado
			return resultado.sucesso(NodeVariavelAssimilar(nome, expr))

		node = resultado.registro(self.op_bin(self.comp_expr, ((TT_PALAVRASCHAVE, 'E'), (TT_PALAVRASCHAVE, 'OU'))))

		if resultado.erro:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,"Esperava 'VAR', 'SE', 'PARA', 'ENQUANTO', 'FUNÇÃO', inteiro, real, identificador, '+', '-', '(', '[' ou 'NÃO'"))

		return resultado.sucesso(node)

	def comp_expr(self):
		resultado = ResultadoDoParser()

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, 'NÃO'):
			op_tok = self.tok_atual
			resultado.registrar_avanco()
			self.avancar()

			node = resultado.registro(self.comp_expr())
			if resultado.erro: return resultado
			return resultado.sucesso(NodeOpUni(op_tok, node))
		
		node = resultado.registro(self.op_bin(self.arith_expr, (TT_EIG, TT_DIF, TT_MNQ, TT_MIQ, TT_MNQIGU, TT_MIQIGU)))
		
		if resultado.erro:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,"Estava esperando um inteiro, real, identificador, '+', '-', '(', '[', 'SE', 'PARA', 'ENQUANTO', 'FUNÇÃO' or 'NÃO'"))

		return resultado.sucesso(node)

	def arith_expr(self):
		return self.op_bin(self.term, (TT_MAI, TT_MEN))

	def term(self):
		return self.op_bin(self.factor, (TT_MUL, TT_DIV))

	def factor(self):
		resultado = ResultadoDoParser()
		tok = self.tok_atual

		if tok.tipo in (TT_MAI, TT_MEN):
			resultado.registrar_avanco()
			self.avancar()
			factor = resultado.registro(self.factor())
			if resultado.erro: return resultado
			return resultado.sucesso(NodeOpBin(tok, factor))

		return self.power()

	def power(self):
		return self.op_bin(self.call, (TT_POT, ), self.factor)

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
						"Estava esperando ')', 'VAR', 'SE', 'PARA', 'ENQUANTO', 'FUNÇÃO', inteiro, real, identificador, '+', '-', '(', '[' ou 'NÃO'"
					))

				while self.tok_atual.tipo == TT_VIRGULA:
					resultado.registrar_avanco()
					self.avancar()

					nodes_argumentos.append(resultado.registro(self.expr()))
					if resultado.erro: return resultado

				if self.tok_atual.tipo != TT_FECPARENT:
					return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Esperava ',' ou ')'"))

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
			if self.tok_atual.tipo == TT_ABRPARENT:
				resultado.registrar_avanco()
				self.avancar()
				return resultado.sucesso(expr)
			else: return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,"Estava esperando um ')'"))

		elif tok.tipo == TT_ABRCOLCHE:
			list_expr = resultado.registro(self.list_expr())
			if resultado.erro: return resultado
			return resultado.sucesso(list_expr)
		
		elif tok.combinam(TT_PALAVRASCHAVE, 'SE'):
			se_expr = resultado.registro(self.se_expr())
			if resultado.erro: return resultado
			return resultado.sucesso(se_expr)

		elif tok.combinam(TT_PALAVRASCHAVE, 'PARA'):
			para_expr = resultado.registro(self.para_expr())
			if resultado.erro: return resultado
			return resultado.sucesso(para_expr)

		elif tok.combinam(TT_PALAVRASCHAVE, 'ENQUANTO'):
			enquanto_expr = resultado.registro(self.enquanto_expr())
			if resultado.erro: return resultado
			return resultado.sucesso(enquanto_expr)

		elif tok.combinam(TT_PALAVRASCHAVE, 'FUNÇÃO'):
			func_def = resultado.registro(self.func_def())
			if resultado.erro: return resultado
			return resultado.sucesso(func_def)

		return resultado.falha(ErroDeSintaxe(tok.inicio, tok.fim,"Estava esperando um inteiro, real, identificador, '+', '-', '(', '[', SE', 'PARA', 'ENQUANTO', 'FUNÇÃO'"))

	def list_expr(self):
		resultado = ResultadoDoParser()
		element_nodes = []
		inicio = self.tok_atual.inicio.copia()

		if self.tok_atual.tipo != TT_ABRCOLCHE:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Esperava '['"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo == TT_FECCOLCHE:
			resultado.registrar_avanco()
			self.avancar()
		else:
			element_nodes.append(resultado.registro(self.expr()))
			if resultado.erro:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,"Esperava ']', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'"))

			while self.tok_atual.tipo == TT_VIRGULA:
				resultado.registrar_avanco()
				self.avancar()

				element_nodes.append(resultado.registro(self.expr()))
				if resultado.erro: return resultado

			if self.tok_atual.tipo != TT_FECCOLCHE:
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Esperava ',' ou ']'"))

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

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, 'SENÃO'):
			resultado.registrar_avanco()
			self.avancar()

			if self.tok_atual.tipo == TT_NOVALINHA:
				resultado.registrar_avanco()
				self.avancar()

				statements = resultado.registro(self.statements())
				if resultado.erro: return resultado
				caso_senao = (statements, True)

				if self.tok_atual.combinam(TT_PALAVRASCHAVE, 'FIM'):
					resultado.registrar_avanco()
					self.avancar()
				else: return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,"Estava esperando um 'FIM'"))
			else:
				expr = resultado.registro(self.statement())
				if resultado.erro: return resultado
				caso_senao = (expr, False)

		return resultado.sucesso(caso_senao)

	def se_expr_b_ou_c(self):
		resultado = ResultadoDoParser()
		casos, caso_senao = [], None

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, 'SENÃOSE'):
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
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Esperava '{case_keyword}'"))

		resultado.registrar_avanco()
		self.avancar()

		condicao = resultado.registro(self.expr())
		if resultado.erro: return resultado

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, 'ENTÃO'):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Esperava 'ENTÃO'"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo == TT_NOVALINHA:
			resultado.registrar_avanco()
			self.avancar()

			statements = resultado.registro(self.statements())
			if resultado.erro: return resultado
			casos.append((condicao, statements, True))

			if self.tok_atual.combinam(TT_PALAVRASCHAVE, 'FIM'):
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

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, 'PARA'):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Esperava 'PARA'"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo != TT_IDE:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Esperava um identificador"))

		nome = self.tok_atual
		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo != TT_IGU:
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Esperava '='"))
		
		resultado.registrar_avanco()
		self.avancar()

		inicio = resultado.registro(self.expr())
		if resultado.erro: return resultado

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, 'CADA'):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Esperava 'CADA'"))
		
		resultado.registrar_avanco()
		self.avancar()

		fim = resultado.registro(self.expr())
		if resultado.erro: return resultado

		if self.tok_atual.combinam(TT_PALAVRASCHAVE, 'PASSO'):
			resultado.registrar_avanco()
			self.avancar()

			passo = resultado.registro(self.expr())
			if resultado.erro: return resultado
		else: passo = None

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, 'ENTÃO'):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Esperava 'ENTÃO'"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo == TT_NOVALINHA:
			resultado.registrar_avanco()
			self.avancar()

			body = resultado.registro(self.statements())
			if resultado.erro: return resultado

			if not self.tok_atual.combinam(TT_PALAVRASCHAVE, 'FIM'):
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Esperava 'FIM'"))

			resultado.registrar_avanco()
			self.avancar()

			return resultado.sucesso(NodePara(nome, inicio, fim, passo, body, True))
		
		body = resultado.registro(self.statement())
		if resultado.erro: return resultado

		return resultado.sucesso(NodePara(nome, inicio, fim, passo, body, False))

	def enquanto_expr(self):
		resultado = ResultadoDoParser()

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, 'ENQUANTO'):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Estava esperando 'ENQUANTO'"))

		resultado.registrar_avanco()
		self.avancar()

		condicao = resultado.registro(self.expr())
		if resultado.erro: return resultado

		if not self.tok_atual.combinam(TT_PALAVRASCHAVE, 'ENTÃO'):
			return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Estava esperando 'ENTÃO'"))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.tipo == TT_NOVALINHA:
			resultado.registrar_avanco()
			self.avancar()

			corpo = resultado.registro(self.statements())
			if resultado.erro: return resultado

			if not self.tok_atual.combinam(TT_PALAVRASCHAVE, 'FIM'):
				return resultado.falha(ErroDeSintaxe(self.tok_atual.inicio, self.tok_atual.fim,f"Estava esperando 'FIM'"))

			resultado.registrar_avanco()
			self.avancar()

			return resultado.sucesso(NodeEnquanto(condicao, corpo, True))
		
		corpo = resultado.registro(self.statement())
		if resultado.erro: return resultado

		return resultado.sucesso(NodeEnquanto(condicao, corpo, False))

	def func_def(self):
		resultado = ResultadoDoParser()

		if not self.tok_atual.matches(TT_PALAVRASCHAVE, 'FUN'):
			return resultado.falha(ErroDeSintaxe(
				self.tok_atual.inicio, self.tok_atual.fim,
				f"Expected 'FUN'"
			))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.type == TT_IDENTIFIER:
			var_name_tok = self.tok_atual
			resultado.registrar_avanco()
			self.avancar()
			if self.tok_atual.type != TT_LPAREN:
				return resultado.falha(ErroDeSintaxe(
					self.tok_atual.inicio, self.tok_atual.fim,
					f"Expected '('"
				))
		else:
			var_name_tok = None
			if self.tok_atual.type != TT_LPAREN:
				return resultado.falha(ErroDeSintaxe(
					self.tok_atual.inicio, self.tok_atual.fim,
					f"Expected identifier or '('"
				))
		
		resultado.registrar_avanco()
		self.avancar()
		arg_name_toks = []

		if self.tok_atual.type == TT_IDENTIFIER:
			arg_name_toks.append(self.tok_atual)
			resultado.registrar_avanco()
			self.avancar()
			
			while self.tok_atual.type == TT_COMMA:
				resultado.registrar_avanco()
				self.avancar()

				if self.tok_atual.type != TT_IDENTIFIER:
					return resultado.falha(ErroDeSintaxe(
						self.tok_atual.inicio, self.tok_atual.fim,
						f"Expected identifier"
					))

				arg_name_toks.append(self.tok_atual)
				resultado.registrar_avanco()
				self.avancar()
			
			if self.tok_atual.type != TT_ABRPARENT:
				return resultado.falha(ErroDeSintaxe(
					self.tok_atual.inicio, self.tok_atual.fim,
					f"Expected ',' or ')'"
				))
		else:
			if self.tok_atual.type != TT_ABRPARENT:
				return resultado.falha(ErroDeSintaxe(
					self.tok_atual.inicio, self.tok_atual.fim,
					f"Expected identifier or ')'"
				))

		resultado.registrar_avanco()
		self.avancar()

		if self.tok_atual.type == TT_ARROW:
			resultado.registrar_avanco()
			self.avancar()

			body = resultado.registro(self.expr())
			if resultado.error: return resultado

			return resultado.sucesso(FuncDefNode(
				var_name_tok,
				arg_name_toks,
				body,
				True
			))
		
		if self.tok_atual.type != TT_NEWLINE:
			return resultado.falha(ErroDeSintaxe(
				self.tok_atual.inicio, self.tok_atual.fim,
				f"Expected '->' or NEWLINE"
			))

		resultado.registrar_avanco()
		self.avancar()

		body = resultado.registro(self.statements())
		if resultado.error: return resultado

		if not self.tok_atual.matches(TT_PALAVRASCHAVE, 'END'):
			return resultado.falha(ErroDeSintaxe(
				self.tok_atual.inicio, self.tok_atual.fim,
				f"Expected 'END'"
			))

		resultado.registrar_avanco()
		self.avancar()
		
		return resultado.sucesso(FuncDefNode(
			var_name_tok,
			arg_name_toks,
			body,
			False
		))

	###################################

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

#######################################
# VALORES
#######################################

class Valor:
	def __init__(self):
		self.fazer_posicao()
		self.fazer_contexto()

	def fazer_posicao(self, inicio=None, fim=None):
		self.inicio = inicio
		self.fim = fim
		return self

	def fazer_contexto(self, contexto=None):
		self.contexto = contexto
		return self

	def mais(self, outro):
		return None, self.operacao_ilegal(outro)

	def subtraido_por(self, outro):
		return None, self.operacao_ilegal(outro)

	def multiplicado_por(self, outro):
		return None, self.operacao_ilegal(outro)

	def dividido_por(self, outro):
		return None, self.operacao_ilegal(outro)

	def elevado_a(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_igualdade(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_diferenca(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_menor_que(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_maior_que(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_menor_igual_que(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_maior_igual_que(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_negacao(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_AND(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_OR(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_NAND(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_NOR(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_XOR(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_XNOR(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_condicional(self, outro):
		return None, self.operacao_ilegal(outro)

	def comparar_bicondicional(self, outro):
		return None, self.operacao_ilegal(outro)

	def executar(self, args):
		return ResultadoDaRT().falha(self.operacao_ilegal())

	def copia(self):
		raise Exception('Nenhum método de cópia definido.')

	def e_verdade(self):
		return False

	def operacao_ilegal(self, outro=None):
		if not outro: outro = self
		return ErroRT(self.inicio, outro.fim,'Operação Ilegal',self.contexto)

class Numero(Valor):
	def __init__(self, valor):
		super().__init__()
		self.valor = valor

	def mais(self, outro):
		if isinstance(outro, Numero):
			return Numero(self.valor + outro.valor).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def subtraido_por(self, outro):
		if isinstance(outro, Numero):
			return Numero(self.valor - outro.valor).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def multiplicado_por(self, outro):
		if isinstance(outro, Numero):
			return Numero(self.valor * outro.valor).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def dividido_por(self, outro):
		if isinstance(outro, Numero):
			if outro.valor == 0:
				return None, ErroRT(outro.inicio, outro.fim,'Você não sabe que é impossível dividir por zero??',self.contexto)
			return Numero(self.valor / outro.valor).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def elevado_a(self, outro):
		if isinstance(outro, Numero):
			return Numero(self.valor ** outro.valor).fazer_contexto(self.contexto), None
		else:
			return None, Valor.operacao_ilegal(self, outro)

	def comparar_igualdade(self, outro):
		if isinstance(outro, Numero):
			return Numero(int(self.valor == outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_diferenca(self, outro):
		if isinstance(outro, Numero):
			return Numero(int(self.valor != outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_menor_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(int(self.valor < outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_maior_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(int(self.valor > outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_menor_igual_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(int(self.valor <= outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_maior_igual_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(int(self.valor >= outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_negacao(self):
		return Numero(1 if self.valor == 0 else 0).fazer_contexto(self.contexto), None

	def comparar_AND(self, outro):
		if isinstance(outro, Numero):
			return Numero(int(self.valor and outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_OR(self, outro):
		if isinstance(outro, Numero):
			return Numero(int(self.valor or outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_NAND(self, outro):
		if isinstance(outro, Numero):
			return Numero(-int(self.valor and outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_NOR(self, outro):
		if isinstance(outro, Numero):
			return Numero(-int(self.valor or outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_XOR(self, outro):
		if isinstance(outro, Numero):
			return Numero(xor(self.valor,outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_XNOR(self, outro):
		if isinstance(outro, Numero):
			return Numero(xor(self.valor,outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_condicional(self, outro):
		if isinstance(outro, Numero):
			return Numero(int(self.valor or outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_bicondicional(self, outro):
		if isinstance(outro, Numero):
			return Numero(int(self.valor or outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def copia(self):
		copia = Numero(self.valor)
		copia.fazer_posicao(self.inicio, self.fim)
		copia.fazer_contexto(self.contexto)
		return copia

	def e_verdade(self): return self.valor != 0

	def __str__(self): return str(self.valor)
	
	def __repr__(self): return str(self.valor)

Numero.nulo = Numero(0)
Numero.falso = Numero(0)
Numero.verdadeiro = Numero(1)
Numero.pi = Numero(3.14)

class Texto(Valor):
	def __init__(self, valor):
		super().__init__()
		self.valor = valor

	def mais(self, outro):
		if isinstance(outro, Texto):
			return Texto(self.valor + outro.valor).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def multiplicado_por(self, outro):
		if isinstance(outro, Numero):
			return Texto(self.valor * outro.valor).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def e_verdade(self):
		return len(self.valor) > 0

	def copia(self):
		copia = Texto(self.valor)
		copia.fazer_posicao(self.inicio, self.fim)
		copia.fazer_contexto(self.contexto)
		return copia

	def __str__(self): return self.valor

	def __repr__(self): return self.valor

class Lista(Valor):
	def __init__(self, elementos):
		super().__init__()
		self.elementos = elementos

	def mais(self, outro):
		nova_lista = self.copia()
		nova_lista.elementos.append(outro)
		return nova_lista, None

	def subtraido_por(self, outro):
		if isinstance(outro, Numero):
			nova_lista = self.copia()
			try:
				nova_lista.elementos.pop(outro.valor)
				return nova_lista, None
			except:
				return None, ErroRT(outro.inicio, outro.fim,
					'Element at this index could not be removed from list because index is out of bounds',
					self.contexto
				)
		else:
			return None, Valor.operacao_ilegal(self, outro)

	def multiplicado_por(self, outro):
		if isinstance(outro, List):
			nova_lista = self.copia()
			nova_lista.elementos.extender(outro.elementos)
			return nova_lista, None
		else: return None, Valor.operacao_ilegal(self, outro)

	def dividido_por(self, outro):
		if isinstance(outro, Numero):
			try:
				return self.elementos[outro.valor], None
			except:
				return None, ErroRT(outro.inicio, outro.fim,
					'Element at this index could not be retrieved from list because index is out of bounds',
					self.contexto
				)
		else:
			return None, Valor.operacao_ilegal(self, outro)
	
	def copia(self):
		copia = Lista(self.elementos)
		copia.fazer_posicao(self.inicio, self.fim)
		copia.fazer_contexto(self.contexto)
		return copia

	def __str__(self): return ", ".join([str(x) for x in self.elementos])

	def __repr__(self): return f'[{", ".join([repr(x) for x in self.elementos])}]'

#######################################
# FUNÇÕES
#######################################

class FuncaoBase(Valor):
	def __init__(self, nome):
		super().__init__()
		self.nome = nome or "<anônimo>"

	def gerar_novo_contexto(self):
		novo_contexto = Contexto(self.nome, self.contexto, self.inicio)
		novo_contexto.tabela_simbolos = TabelaDeSimbolos(novo_contexto.pai.tabela_simbolos)
		return novo_contexto

	def verificar_argumentos(self, nomes, argumentos):
		resultado = ResultadoDaRT()

		if len(argumentos) > len(nomes):
			return resultado.falha(ErroRT(self.inicio, self.fim,f"{len(argumentos) - len(nomes)} tem argumentos demais sendo passados para \"{self.nome}\"",self.contexto))
		
		if len(argumentos) < len(nomes):
			return resultado.falha(ErroRT(self.inicio, self.fim,f"{len(nomes) - len(argumentos)} tem poucos argumentos sendo passados para \"{self.nome}\"",self.contexto))

		return resultado.sucesso(None)

	def popular_argumentos(self, nomes, argumentos, exec_ctx):
		for i in range(len(argumentos)):
			nome = nomes[i]
			valor = argumentos[i]
			valor.fazer_contexto(exec_ctx)
			exec_ctx.tabela_simbolos.criar(nome, valor)

	def verificar_e_popular_argumentos(self, nomes, argumentos, exec_ctx):
		resultado = ResultadoDaRT()
		resultado.registro(self.verificar_argumentos(nomes, argumentos))
		if resultado.deve_retornar(): return resultado
		self.popular_argumentos(nomes, argumentos, exec_ctx)
		return resultado.sucesso(None)

class Funcao(FuncaoBase):
	def __init__(self,nome,corpo,argumentos,retornar_automaticamente):
		super().__init__(nome)
		self.corpo = corpo
		self.argumentos = argumentos
		self.retornar_automaticamente = retornar_automaticamente
	
	def executar(self,argumentos):
		resultado = ResultadoDaRT()
		interpretar = Interpretador()
		executar_contexto = self.gerar_novo_contexto()
		
		resultado.registro(self.verificar_e_popular_argumentos(self.argumentos,argumentos,executar_contexto))
		if resultado.deve_retornar(): return resultado
		
		valor = resultado.registro(interpretar.visitar(self.corpo,executar_contexto))
		if resultado.deve_retornar() and resultado.valor_retornado_da_funcao == None: return resultado
		
		resultado.valor = (valor if self.retornar_automaticamente else None) or resultado.valor_retornado_da_funcao or Numero.nulo
		return resultado.sucesso(resultado.valor)
		
	def copia(self):
		copia = Funcao(self.nome,self.corpo,self.argumentos,self.retornar_automaticamente)
		copia.fazer_contexto(self.contexto)
		copia.fazer_posicao(self.inicio,self.fim)
		return copia
	
	def __repr__(self):
		return f'<função {self.nome}>'

class FuncaoInstalada(FuncaoBase):
	def __init__(self, nome):
		super().__init__(nome)

	def execute(self, args):
		resultado = ResultadoDaRT()
		exec_ctx = self.gerar_novo_contexto()

		method_name = f'executar_{self.nome}'
		method = getattr(self, method_name, self.no_visit_method)

		resultado.registro(self.verificar_e_popular_argumentos(method.arg_names, args, exec_ctx))
		if resultado.deve_retornar(): return resultado

		return_value = resultado.registro(method(exec_ctx))
		if resultado.deve_retornar(): return resultado
		return resultado.sucesso(return_value)
	
	def no_visit_method(self, node, contexto):
		raise Exception(f'Nenhuma função \"executar_{self.nome}\" foi definida.')

	def copia(self):
		copia = FuncaoInstalada(self.nome)
		copia.fazer_contexto(self.contexto)
		copia.fazer_posicao(self.inicio, self.fim)
		return copia

	def __repr__(self):
		return f"<built-in function {self.nome}>"

	def executar_escrever(self, exec_ctx):
		print(str(exec_ctx.tabela_simbolos.obter('valor')))
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_escrever.arg_names = ['valor']
	
	def executar_escrever_ret(self, exec_ctx):
		return ResultadoDaRT().sucesso(Texto(str(exec_ctx.tabela_simbolos.obter('valor'))))
	executar_escrever_ret.arg_names = ['valor']

	def executar_ler(self, exec_ctx):
		texto = input()
		return ResultadoDaRT().sucesso(Texto(texto))
	executar_ler.arg_names = []

	def executar_ler_inteiro(self, exec_ctx):
		while True:
			texto = input()
			try: number = int(texto); break
			except ValueError: print(f"'{texto}' precisa ser um número do tipo inteiro!")
		return ResultadoDaRT().sucesso(Numero(number))
	executar_ler_inteiro.arg_names = []

	def executar_limpar(self, exec_ctx):
		os.system('cls' if os.name == 'nt' else 'clear') 
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_limpar.arg_names = []

	def executar_pausar(self, exec_ctx):
		input()
		return ResultadoDaRT().sucesso(Texto(""))
	executar_pausar.arg_names = []

	def executar_esperar(self, exec_ctx):
		time.sleep(exec_ctx.tabela_simbolos.obter('segundos').valor)
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_esperar.arg_names = ["segundos"]

	def executar_e_um_numero(self, exec_ctx):
		e_um_numero = isinstance(exec_ctx.tabela_simbolos.obter("valor"), Numero)
		return ResultadoDaRT().sucesso(Numero.verdadeiro if e_um_numero else Numero.falso)
	executar_e_um_numero.arg_names = ["valor"]

	def executar_e_um_texto(self, exec_ctx):
		e_um_numero = isinstance(exec_ctx.tabela_simbolos.obter("valor"), String)
		return ResultadoDaRT().sucesso(Numero.verdadeiro if e_um_numero else Numero.falso)
	executar_e_um_texto.arg_names = ["valor"]

	def executar_e_uma_lista(self, exec_ctx):
		e_um_numero = isinstance(exec_ctx.tabela_simbolos.obter("valor"), List)
		return ResultadoDaRT().sucesso(Numero.verdadeiro if e_um_numero else Numero.falso)
	executar_e_uma_lista.arg_names = ["valor"]

	def executar_e_uma_funcao(self, exec_ctx):
		e_um_numero = isinstance(exec_ctx.tabela_simbolos.obter("valor"), FuncaoBase)
		return ResultadoDaRT().sucesso(Numero.verdadeiro if e_um_numero else Numero.falso)
	executar_e_uma_funcao.arg_names = ["valor"]

	def executar_adicionar(self, exec_ctx):
		lista = exec_ctx.tabela_simbolos.obter("list")
		valor = exec_ctx.tabela_simbolos.obter("valor")

		if not isinstance(lista, Lista):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,"O primeiro argumento precisa ser uma lista",exec_ctx))

		lista.elementos.append(valor)
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_adicionar.arg_names = ["list", "valor"]

	def executar_remover(self, exec_ctx):
		lista = exec_ctx.tabela_simbolos.obter("list")
		index = exec_ctx.tabela_simbolos.obter("index")

		if not isinstance(lista, Lista):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,"O primeiro argumento precisa ser uma lista",exec_ctx))
		if not isinstance(index, Numero):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,"O segundo argumento também precisa ser uma lista",exec_ctx))

		try:
			element = lista.elementos.pop(index.valor)
		except:
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,'Element at this index could not be removed from list because index is out of bounds',exec_ctx))
		return ResultadoDaRT().sucesso(element)
	executar_remover.arg_names = ["list", "index"]

	def executar_extender(self, exec_ctx):
		listA = exec_ctx.tabela_simbolos.obter("listA")
		listB = exec_ctx.tabela_simbolos.obter("listB")

		if not isinstance(listA, List):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,"O primeiro argumento precisa ser uma lista",exec_ctx))

		if not isinstance(listB, List):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,"O segundo argumento também precisa ser uma lista",exec_ctx))

		listA.elementos.extend(listB.elementos)
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_extender.arg_names = ["listA", "listB"]

	def executar_tamanho(self, exec_ctx):
		lista = exec_ctx.tabela_simbolos.obter("lista")

		if not isinstance(lista, Lista):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,"Argumento precisa ser uma lista",exec_ctx))
		return ResultadoDaRT().sucesso(Numero(len(lista.elementos)))
	executar_tamanho.arg_names = ["list"]

	def executar_obter_hora_atual(self, exec_ctx):
		print(datetime.today().strftime("%d / %m / %Y"))
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_tamanho.arg_names = []

	def executar_obter_data_atual(self, exec_ctx):
		print(datetime.today().strftime("%H : %M : %S"))
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_tamanho.arg_names = []

	def executar_executar(self, exec_ctx):
		arquivo = exec_ctx.tabela_simbolos.obter("arquivo")

		if not isinstance(arquivo, Texto):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,"Argumento deve ser o caminho para o arquivo em texto",exec_ctx))

		arquivo = arquivo.valor

		try:
			with open(arquivo, "r") as f: script = f.read()
		except Exception as e:
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,f"Falha ao carregar o script \"{arquivo}\"\n" + str(e),exec_ctx))
		_, erro = executar(arquivo, script)
		
		if erro:
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,f"Falha ao terminar de executar o script \"{arquivo}\"\n" + erro.como_texto(),exec_ctx))
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_executar.arg_names = ["arquivo"]

for i in ('escrever','escrever_ret','ler','ler_inteiro','limpar','pausar','esperar','e_um_numero','e_um_texto','e_uma_lista','e_uma_funcao',
	'adicionar','remover','extender','tamanho','obter_hora_atual','obter_data_atual','executar'):
	exec(f'FuncaoInstalada.{i} = FuncaoInstalada("{i}")')

#######################################
# CONTEXTO
#######################################

class Contexto:
	def __init__(self,mostrar_nome=None,pai=None,posicao_do_pai=None):
		self.mostrar_nome = mostrar_nome
		self.pai = pai
		self.posicao_do_pai = posicao_do_pai
		self.tabela_simbolos = None
		
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

#######################################
# EXECUTAR
#######################################

class Interpretador:
	def visitar(self, node, contexto):
		method_name = f'visitar_{type(node).__name__}'
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, contexto)

	def no_visit_method(self, node, contexto):
		raise Exception(f'Nenhuma função "visitar_{type(node).__name__}" foi definida')

	###################################

	def visitar_NodeNumero(self, node, contexto):
		return ResultadoDaRT().sucesso(Numero(node.token.valor).fazer_contexto(contexto).fazer_posicao(node.inicio, node.fim))

	def visitar_NodeTexto(self, node, contexto):
		return ResultadoDaRT().sucesso(Texto(node.token.valor).fazer_contexto(contexto).fazer_posicao(node.inicio, node.fim))

	def visitar_NodeLista(self, node, contexto):
		resultado = ResultadoDaRT()
		lista = []

		for elemento in node.elementos:
			lista.append(resultado.registro(self.visitar(elemento, contexto)))
			if resultado.deve_retornar(): return resultado

		return resultado.sucesso(Lista(lista).fazer_contexto(contexto).fazer_posicao(node.inicio, node.fim))

	def visitar_NodeVariavelAcesso(self, node, contexto):
		resultado = ResultadoDaRT()
		nome = node.nome.valor
		valor = contexto.tabela_simbolos.obter(nome)
		if not valor: return resultado.falha(ErroRT(node.inicio, node.fim,f"Não existe nenhuma variável chamada \"{nome}\".",contexto))
		valor = valor.copia().fazer_posicao(node.inicio, node.fim).fazer_contexto(contexto)
		return resultado.sucesso(valor)

	def visitar_NodeVariavelAssimilar(self, node, contexto):
		resultado = ResultadoDaRT()
		nome = node.nome.valor
		valor = resultado.registro(self.visitar(node.valor, contexto))
		if resultado.deve_retornar(): return resultado
		contexto.tabela_simbolos.criar(nome, valor)
		return resultado.sucesso(valor)

	def visitar_NodeOpUni(self, node, contexto):
		resultado = ResultadoDaRT()
		number = resultado.registro(self.visitar(node.node, contexto))
		if resultado.deve_retornar(): return resultado

		erro = None
		if node.op_tok.tipo == TT_MEN: number, erro = number.multiplicado_por(Numero(-1))
		elif node.op_tok.combinam(TT_PALAVRASCHAVE, 'NÃO'): number, erro = number.comparar_negacao()

		if erro: return resultado.falha(erro)
		else: return resultado.sucesso(number.fazer_posicao(node.inicio, node.fim))

	def visitar_NodeOpBin(self, node, contexto):
		resultado = ResultadoDaRT()
		esquerdo = resultado.registro(self.visitar(node.node_esquerdo, contexto))
		if resultado.deve_retornar(): return resultado
		direito = resultado.registro(self.visitar(node.node_direito, contexto))
		if resultado.deve_retornar(): return resultado

		if node.tok_op.tipo == TT_MAI: valor, erro = esquerdo.mais(direito)
		elif node.tok_op.tipo == TT_MEN: valor, erro = esquerdo.subtraido_por(direito)
		elif node.tok_op.tipo == TT_MUL: valor, erro = esquerdo.multiplicado_por(direito)
		elif node.tok_op.tipo == TT_DIV: valor, erro = esquerdo.dividido_por(direito)
		elif node.tok_op.tipo == TT_POT: valor, erro = esquerdo.elevado_a(direito)
		elif node.tok_op.tipo == TT_EIG: valor, erro = esquerdo.comparar_igualdade(direito)
		elif node.tok_op.tipo == TT_DIF: valor, erro = esquerdo.comparar_diferenca(direito)
		elif node.tok_op.tipo == TT_MNQ: valor, erro = esquerdo.comparar_menor_que(direito)
		elif node.tok_op.tipo == TT_MIQ: valor, erro = esquerdo.comparar_maior_que(direito)
		elif node.tok_op.tipo == TT_MNQIGU: valor, erro = esquerdo.comparar_menor_igual_que(direito)
		elif node.tok_op.tipo == TT_MIQIGU: valor, erro = esquerdo.comparar_maior_igual_que(direito)
		elif node.tok_op.combinam(TT_PALAVRASCHAVE, ('E','e')): valor, erro = esquerdo.comparar_AND(direito)
		elif node.tok_op.combinam(TT_PALAVRASCHAVE, ('OU','ou')): valor, erro = esquerdo.comparar_OR(direito)
		elif node.tok_op.combinam(TT_PALAVRASCHAVE, ('NE','ne')): valor, erro = esquerdo.comparar_NAND(direito)
		elif node.tok_op.combinam(TT_PALAVRASCHAVE, ('NOU','nou')): valor, erro = esquerdo.comparar_NOR(direito)
		elif node.tok_op.combinam(TT_PALAVRASCHAVE, ('XOU','xou')): valor, erro = esquerdo.comparar_XOR(direito)
		elif node.tok_op.combinam(TT_PALAVRASCHAVE, ('XNOU','xnou')): valor, erro = esquerdo.comparar_XNOR(direito)
		elif node.tok_op.combinam(TT_PALAVRASCHAVE, '=>'): valor, erro = esquerdo.comparar_condicional(direito)
		elif node.tok_op.combinam(TT_PALAVRASCHAVE, '<=>'): valor, erro = esquerdo.comparar_bicondicional(direito)

		if erro: return resultado.falha(valor)
		else: return resultado.sucesso(valor.fazer_posicao(node.inicio, node.fim))

	def visitar_NodeSe(self, node, contexto):
		resultado = ResultadoDaRT()

		for condition, expr, deve_retornar_nulo in node.casos:
			condition_value = resultado.registro(self.visitar(condition, contexto))
			if resultado.deve_retornar(): return resultado

			if condition_value.e_verdade():
				valor_expr = resultado.registro(self.visitar(expr, contexto))
				if resultado.deve_retornar(): return resultado
				return resultado.sucesso(Numero.nulo if deve_retornar_nulo else valor_expr)

		if node.senao:
			expr, deve_retornar_nulo = node.senao
			valor_expr = resultado.registro(self.visitar(expr, contexto))
			if resultado.deve_retornar(): return resultado
			return resultado.sucesso(Numero.nulo if deve_retornar_nulo else valor_expr)

		return resultado.sucesso(Numero.nulo)

	def visitar_NodeEnquanto(self, node, contexto):
		resultado = ResultadoDaRT()
		elementos = []

		while True:
			condicao = resultado.registro(self.visitar(node.node_condicao, contexto))
			if resultado.deve_retornar(): return resultado

			if not condicao.is_true():
				break

			valor = resultado.registro(self.visitar(node.node_corpo, contexto))
			if resultado.deve_retornar() and resultado.loop_deve_continuar == False and resultado.loop_deve_quebrar == False: return resultado
			if resultado.loop_deve_continuar: continue
			if resultado.loop_deve_quebrar: break
			elementos.append(valor)

		return resultado.sucesso(Numero.nulo if node.retornar_automaticamente else Lista(elementos).fazer_contexto(contexto).fazer_posicao(node.inicio, node.fim))

	def visitar_NodePara(self, node, contexto):
		resultado = ResultadoDaRT()
		elementos = []

		inicio = resultado.registro(self.visitar(node.node_inicio, contexto))
		if resultado.deve_retornar(): return resultado

		fim = resultado.registro(self.visitar(node.node_final, contexto))
		if resultado.deve_retornar(): return resultado

		if node.node_passo:
			passo = resultado.registro(self.visitar(node.node_passo, contexto))
			if resultado.deve_retornar(): return resultado
		else: passo = Numero(1)

		i = inicio.valor

		if passo.valor >= 0: condition = lambda: i < fim.valor
		else: condition = lambda: i > fim.valor
		
		while condition():
			contexto.tabela_simbolos.criar(node.node_nome.valor, Numero(i))
			i += passo.valor

			valor = resultado.registro(self.visitar(node.node_corpo, contexto))
			if resultado.deve_retornar() and resultado.loop_deve_continuar == False and resultado.loop_deve_quebrar == False: return resultado
			
			if resultado.loop_deve_continuar: continue
			if resultado.loop_deve_quebrar: break

			elementos.append(valor)

		return resultado.sucesso(Numero.nulo if node.retornar_automaticamente else Lista(elementos).fazer_contexto(contexto).fazer_posicao(node.inicio, node.fim))

	def visitar_NodeFuncao(self, node, contexto):
		resultado = ResultadoDaRT()

		nome = node.node_nome.valor if node.node_nome else None
		body_node = node.body_node
		arg_names = [arg_name.valor for arg_name in node.arg_name_toks]
		func_value = Function(nome, body_node, arg_names, node.retornar_automaticamente).fazer_contexto(contexto).fazer_posicao(node.inicio, node.fim)
		
		if node.node_nome: contexto.tabela_simbolos.set(nome, func_value)

		return resultado.sucesso(func_value)

	def visitar_NodeChamar(self, node, contexto):
		resultado = ResultadoDaRT()
		args = []

		valor = resultado.registro(self.visitar(node.node_chamado, contexto))
		if resultado.deve_retornar(): return resultado
		valor = valor.copia().fazer_posicao(node.inicio, node.fim)

		for argumento in node.nodes:
			args.append(resultado.registro(self.visitar(argumento, contexto)))
			if resultado.deve_retornar(): return resultado

		return_value = resultado.registro(valor.execute(args))
		if resultado.deve_retornar(): return resultado
		return_value = return_value.copia().fazer_posicao(node.inicio, node.fim).fazer_contexto(contexto)
		return resultado.sucesso(return_value)

	def visitar_NodeRetornar(self, node, contexto):
		resultado = ResultadoDaRT()

		if node.node_to_return:
			valor = resultado.registro(self.visitar(node.node_to_return, contexto))
			if resultado.deve_retornar(): return resultado
		else: valor = Numero.nulo
		
		return resultado.sucesso_do_retornar(valor)

	def visitar_NodeContinuar(self, node, contexto):
		return ResultadoDaRT().sucesso_do_continuar()

	def visitar_NodeQuebrar(self, node, contexto):
		return ResultadoDaRT().sucesso_do_quebrar()

tabela_global_simbolos = TabelaDeSimbolos()
for c in range(2):
	if c == 0: case = "upper"
	else: case = "lower"
	tabela_global_simbolos.criar(eval("'NULO'." + case + "()"), Numero.nulo)
	tabela_global_simbolos.criar(eval("'FALSO'." + case + "()"), Numero.falso)
	tabela_global_simbolos.criar(eval("'VERDADEIRO'." + case + "()"), Numero.verdadeiro)
	tabela_global_simbolos.criar(eval("'PI'." + case + "()"), Numero.pi)
	tabela_global_simbolos.criar(eval("'ESCREVER'." + case + "()"), FuncaoInstalada.escrever)
	tabela_global_simbolos.criar(eval("'ESCREVER_RET'." + case + "()"), FuncaoInstalada.escrever_ret)
	tabela_global_simbolos.criar(eval("'LER'." + case + "()"), FuncaoInstalada.ler)
	tabela_global_simbolos.criar(eval("'LER_INTEIRO'." + case + "()"), FuncaoInstalada.ler_inteiro)
	tabela_global_simbolos.criar(eval("'LIMPAR'." + case + "()"), FuncaoInstalada.limpar)
	tabela_global_simbolos.criar(eval("'CLS'." + case + "()"), FuncaoInstalada.limpar)
	tabela_global_simbolos.criar(eval("'PAUSAR'." + case + "()"), FuncaoInstalada.pausar)
	tabela_global_simbolos.criar(eval("'ESPERAR'." + case + "()"), FuncaoInstalada.esperar)
	tabela_global_simbolos.criar(eval("'E_UM_NUMERO'." + case + "()"), FuncaoInstalada.e_um_numero)
	tabela_global_simbolos.criar(eval("'É_UM_NUMERO'." + case + "()"), FuncaoInstalada.e_um_numero)
	tabela_global_simbolos.criar(eval("'E_UM_NÚMERO'." + case + "()"), FuncaoInstalada.e_um_numero)
	tabela_global_simbolos.criar(eval("'É_UM_NÚMERO'." + case + "()"), FuncaoInstalada.e_um_numero)
	tabela_global_simbolos.criar(eval("'É_UM_TEXTO'." + case + "()"), FuncaoInstalada.e_um_texto)
	tabela_global_simbolos.criar(eval("'E_UM_TEXTO'." + case + "()"), FuncaoInstalada.e_uma_lista)
	tabela_global_simbolos.criar(eval("'É_UM_TEXTO'." + case + "()"), FuncaoInstalada.e_um_texto)
	tabela_global_simbolos.criar(eval("'É_UMA_FUNÇÃO'." + case + "()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval("'E_UMA_FUNÇÃO'." + case + "()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval("'E_UMA_FUNCÃO'." + case + "()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval("'E_UMA_FUNCAO'." + case + "()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval("'É_UMA_FUNCÃO'." + case + "()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval("'E_UMA_FUNÇAO'." + case + "()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval("'ADD'." + case + "()"), FuncaoInstalada.adicionar)
	tabela_global_simbolos.criar(eval("'ADICIONAR'." + case + "()"), FuncaoInstalada.adicionar)
	tabela_global_simbolos.criar(eval("'REMOVER'." + case + "()"), FuncaoInstalada.remover)
	tabela_global_simbolos.criar(eval("'EXTENDER'." + case + "()"), FuncaoInstalada.extender)
	tabela_global_simbolos.criar(eval("'TAMANHO'." + case + "()"), FuncaoInstalada.tamanho)
	tabela_global_simbolos.criar(eval("'OBTER_HORA_ATUAL'." + case + "()"), FuncaoInstalada.obter_hora_atual)
	tabela_global_simbolos.criar(eval("'OBTER_DATA_ATUAL'." + case + "()"), FuncaoInstalada.obter_data_atual)
	tabela_global_simbolos.criar(eval("'EXECUTAR'." + case + "()"), FuncaoInstalada.executar)

def executar(arquivo, texto):
	#CRIAR TOKENS
	lexer = Lexer(arquivo, texto)
	tokens, erro = lexer.criar_tokens()
	if erro: return None, erro
	
	#GERAR ÁRVORE DO PARSER
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.erro: return None, ast.erro
	
	#INTERPRETAR O PROGRAMA
	interpretar = Interpretador()
	contexto = Contexto('<programa>')
	contexto.tabela_simbolos = tabela_global_simbolos
	resultado = interpretar.visitar(ast.node,contexto)
	
	return resultado.valor, resultado.erro