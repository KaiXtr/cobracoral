# -*- coding: utf-8 -*-
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
