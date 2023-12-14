# -*- coding: utf-8 -*-
from keywords_PT import *
from posicao import *

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

	def executar(self, args):
		return ResultadoDaRT().falha(self.operacao_ilegal())

	def copia(self):
		raise Exception(EM_Copy)

	def e_verdade(self):
		return False

	def funcao_ilegal(self, outro):
		return None, self.operacao_ilegal(outro)

	def operacao_ilegal(self, outro=None):
		if not outro: outro = self
		return ErroRT(self.inicio, outro.fim,EM_IlegalOp,self.contexto)

for i in ('mais','subtraido_por','multiplicado_por','dividido_por','resto','elevado_a','radiciacao',
	'intersecao_de','pertence_a','nao_pertence_a',
	'comparar_igualdade','comparar_diferenca','comparar_menor_que','comparar_maior_que','comparar_menor_igual_que','comparar_maior_igual_que',
	'comparar_negacao','comparar_AND','comparar_OR','comparar_NAND','comparar_NOR','comparar_XOR','comparar_XNOR','comparar_condicional','comparar_bicondicional'):
	exec(f"Valor.{i} = Valor.funcao_ilegal")

class Numero(Valor):
	def __init__(self, valor):
		super().__init__()
		self.valor = valor
		self.tipo = TT_INTEIRO

	def mais(self, outro):
		if isinstance(outro, Numero):
			return Numero(self.valor + outro.valor).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(str(self.valor) + outro.valor).fazer_contexto(self.contexto), None
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
				return None, ErroRT(outro.inicio, outro.fim,EM_ZeroDiv,self.contexto)
			return Numero(self.valor / outro.valor).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def resto(self, outro):
		if isinstance(outro, Numero):
			return Numero(self.valor % outro.valor).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def elevado_a(self, outro):
		if isinstance(outro, Numero):
			return Numero(self.valor ** outro.valor).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def radiciacao(self, outro):
		if isinstance(outro, Numero):
			return Numero(self.valor // outro.valor).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_igualdade(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(self.valor == outro.valor)).fazer_contexto(self.contexto), None
		else: return Numero(False).fazer_contexto(self.contexto), None

	def comparar_diferenca(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(self.valor != outro.valor)).fazer_contexto(self.contexto), None
		else: return Numero(True).fazer_contexto(self.contexto), None

	def comparar_menor_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(self.valor < outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(self.valor < len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(self.valor < len(outro.elementos))).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_maior_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(self.valor > outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(self.valor > len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(self.valor > len(outro.elementos))).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_menor_igual_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(self.valor <= outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(self.valor <= len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(self.valor <= len(outro.elementos))).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_maior_igual_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(self.valor >= outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(self.valor >= len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(self.valor >= len(outro.elementos))).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def pertence_a(self, outro):
		if isinstance(outro, Lista):
			return Numero(bool(self.valor in outro.elementos)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def nao_pertence_a(self, outro):
		if isinstance(outro, Lista):
			return Numero(bool(self.valor not in outro.elementos)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_negacao(self):
		return Numero(1 if self.valor == 0 else 0).fazer_contexto(self.contexto), None

	def comparar_AND(self, outro):
		if isinstance(outro, Numero):
			return Numero(True if (self.valor and outro.valor) > 0 else False).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_OR(self, outro):
		if isinstance(outro, Numero):
			return Numero(True if (self.valor or outro.valor) > 0 else False).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_NAND(self, outro):
		if isinstance(outro, Numero):
			return Numero(True if ((-self.valor and -outro.valor) + 1) > 0 else False).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_NOR(self, outro):
		if isinstance(outro, Numero):
			return Numero(True if ((-self.valor or -outro.valor) + 1) > 0 else False).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_XOR(self, outro):
		if isinstance(outro, Numero):
			return Numero(True if (self.valor ^ outro.valor) > 0 else False).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_XNOR(self, outro):
		if isinstance(outro, Numero):
			return Numero(True if (-self.valor ^ -outro.valor) > 0 else False).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_condicional(self, outro):
		if isinstance(outro, Numero):
			return Numero(True if (self.valor or outro.valor) > 0 else False).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_bicondicional(self, outro):
		if isinstance(outro, Numero):
			return Numero(True if (self.valor or outro.valor) > 0 else False).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def copia(self):
		copia = Numero(self.valor)
		copia.fazer_posicao(self.inicio, self.fim)
		copia.fazer_contexto(self.contexto)
		return copia

	def e_verdade(self): return self.valor != 0

	def __str__(self): return str(self.valor)
	
	def __repr__(self): return str(self.valor)

class Texto(Valor):
	def __init__(self, valor):
		super().__init__()
		self.valor = valor

	def mais(self, outro):
		if isinstance(outro, Texto):
			return Texto(self.valor + outro.valor).fazer_contexto(self.contexto), None
		elif isinstance(outro, Numero):
			return Texto(self.valor + str(outro.valor)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def subtraido_por(self, outro):
		if isinstance(outro, Numero):
			lmt = -outro.valor if outro.valor > 0 else len(self.valor)
			return Texto(self.valor[0:lmt]).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def multiplicado_por(self, outro):
		if isinstance(outro, Numero):
			return Texto(self.valor * outro.valor).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_igualdade(self, outro):
		if isinstance(outro, Texto):
			return Numero(bool(self.valor == outro.valor)).fazer_contexto(self.contexto), None
		else: return Numero(False).fazer_contexto(self.contexto), None

	def comparar_diferenca(self, outro):
		if isinstance(outro, Texto):
			return Numero(bool(self.valor != outro.valor)).fazer_contexto(self.contexto), None
		else: return Numero(True).fazer_contexto(self.contexto), None

	def comparar_menor_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(len(self.valor) < outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(len(self.valor) < len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(len(self.valor) < len(outro.elementos))).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_maior_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(len(self.valor) > outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(len(self.valor) > len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(len(self.valor) > len(outro.elementos))).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_menor_igual_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(len(self.valor) <= outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(len(self.valor) <= len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(len(self.valor) <= len(outro.elementos))).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_maior_igual_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(len(self.valor) >= outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(len(self.valor) >= len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(len(self.valor) >= len(outro.elementos))).fazer_contexto(self.contexto), None
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
				return None, ErroRT(outro.inicio, outro.fim,EM_ListBounds,self.contexto)
		else: return None, Valor.operacao_ilegal(self, outro)

	def multiplicado_por(self, outro):
		if isinstance(outro, Lista):
			nova_lista = self.copia()
			nova_lista.elementos.extender(outro.elementos)
			return nova_lista, None
		else: return None, Valor.operacao_ilegal(self, outro)

	def dividido_por(self, outro):
		if isinstance(outro, Numero):
			try:
				return self.elementos[outro.valor], None
			except:
				return None, ErroRT(outro.inicio, outro.fim,EM_ListBounds,self.contexto)
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_igualdade(self, outro):
		if isinstance(outro, Lista):
			return Numero(bool(self.elementos == outro.elementos)).fazer_contexto(self.contexto), None
		else: return Numero(False).fazer_contexto(self.contexto), None

	def comparar_diferenca(self, outro):
		if isinstance(outro, Lista):
			return Numero(bool(self.elementos != outro.elementos)).fazer_contexto(self.contexto), None
		else: return Numero(True).fazer_contexto(self.contexto), None

	def comparar_menor_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(len(self.elementos) < outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(len(self.elementos) < len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(len(self.elementos) < len(outro.elementos))).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_maior_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(len(self.elementos) > outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(len(self.elementos) > len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(len(self.elementos) > len(outro.elementos))).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_menor_igual_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(len(self.elementos) <= outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(len(self.elementos) <= len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(len(self.elementos) <= len(outro.elementos))).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def comparar_maior_igual_que(self, outro):
		if isinstance(outro, Numero):
			return Numero(bool(len(self.elementos) >= outro.valor)).fazer_contexto(self.contexto), None
		elif isinstance(outro, Texto):
			return Numero(bool(len(self.elementos) >= len(outro.valor))).fazer_contexto(self.contexto), None
		elif isinstance(outro, Lista):
			return Numero(bool(len(self.elementos) >= len(outro.elementos))).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def intersecao_de(self, outro):
		if isinstance(outro, Lista):
			return Lista([i for i in self.elementos if i in set(outro.elementos)]).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def pertence_a(self, outro):
		if isinstance(outro, Lista):
			return Numero(bool(self.elementos in outro.elementos)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)

	def nao_pertence_a(self, outro):
		if isinstance(outro, Lista):
			return Numero(bool(self.elementos not in outro.elementos)).fazer_contexto(self.contexto), None
		else: return None, Valor.operacao_ilegal(self, outro)
	
	def copia(self):
		copia = Lista(self.elementos)
		copia.fazer_posicao(self.inicio, self.fim)
		copia.fazer_contexto(self.contexto)
		return copia

	def __str__(self): return ", ".join([str(x) for x in self.elementos])

	def __repr__(self): return f'[{", ".join([repr(x) for x in self.elementos])}]'

Numero.nulo = Numero(0)
Numero.falso = Numero(0)
Numero.verdadeiro = Numero(1)
Numero.pi = Numero(3.14)
