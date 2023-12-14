# -*- coding: utf-8 -*-
import datetime
import time
import os

from tabela_de_simbolos import *
from resultado_da_rt import *
from contexto import *
from valores import *
from erros import *

#######################################
# FUNÇÕES
#######################################

class FuncaoBase(Valor):
	def __init__(self, nome):
		super().__init__()
		self.nome = nome or REPR_FUNC

	def gerar_novo_contexto(self):
		novo_contexto = Contexto(self.nome, self.contexto, self.inicio)
		novo_contexto.tabela_simbolos = TabelaDeSimbolos(novo_contexto.pai.tabela_simbolos)
		return novo_contexto

	def verificar_argumentos(self, nomes, argumentos):
		resultado = ResultadoDaRT()

		if len(argumentos) > len(nomes):
			return resultado.falha(ErroRT(self.inicio, self.fim,f"{len(argumentos) - len(nomes)} {EM_ArgsMuch} \"{self.nome}\"",self.contexto))
		
		if len(argumentos) < len(nomes):
			return resultado.falha(ErroRT(self.inicio, self.fim,f"{len(nomes) - len(argumentos)} {EM_ArgsFew} \"{self.nome}\"",self.contexto))

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
		return REPR_FUNC.format(self.nome)

class FuncaoInstalada(FuncaoBase):
	def __init__(self, nome, args=""):
		super().__init__(nome)
		self.args = args

	def __repr__(self):
		return REPR_BUILTIN.format(self.nome.upper(),self.nome.lower(),self.args)

	def executar(self, args):
		resultado = ResultadoDaRT()
		exec_ctx = self.gerar_novo_contexto()
		method = getattr(self, f'executar_{self.nome}', self.no_visit_method)

		resultado.registro(self.verificar_e_popular_argumentos(method.arg_names, args, exec_ctx))
		if resultado.deve_retornar(): return resultado

		return_value = resultado.registro(method(exec_ctx))
		if resultado.deve_retornar(): return resultado
		return resultado.sucesso(return_value)
	
	def no_visit_method(self, node, contexto):
		raise Exception(EM_NoFunc.format('executar_' + self.nome))

	def copia(self):
		copia = FuncaoInstalada(self.nome)
		copia.fazer_contexto(self.contexto)
		copia.fazer_posicao(self.inicio, self.fim)
		return copia

	def executar_listar(self, exec_ctx):
		print(FUNCOES_LISTA)
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_listar.arg_names = []

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
			except ValueError: print(EM_MustInt)
		return ResultadoDaRT().sucesso(Numero(number))
	executar_ler_inteiro.arg_names = []

	def executar_limpar(self, exec_ctx):
		os.system('cls' if os.name == 'nt' else 'clear') 
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_limpar.arg_names = []

	def executar_pausar(self, exec_ctx):
		input()
		return ResultadoDaRT().sucesso(Texto(""))
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
		e_um_numero = isinstance(exec_ctx.tabela_simbolos.obter("valor"), Texto)
		return ResultadoDaRT().sucesso(Numero.verdadeiro if e_um_numero else Numero.falso)
	executar_e_um_texto.arg_names = ["valor"]

	def executar_e_uma_lista(self, exec_ctx):
		e_um_numero = isinstance(exec_ctx.tabela_simbolos.obter("valor"), Lista)
		return ResultadoDaRT().sucesso(Numero.verdadeiro if e_um_numero else Numero.falso)
	executar_e_uma_lista.arg_names = ["valor"]

	def executar_e_uma_funcao(self, exec_ctx):
		e_um_numero = isinstance(exec_ctx.tabela_simbolos.obter("valor"), FuncaoBase)
		return ResultadoDaRT().sucesso(Numero.verdadeiro if e_um_numero else Numero.falso)
	executar_e_uma_funcao.arg_names = ["valor"]

	def executar_tabela_binario(self, exec_ctx):
		exp = None
		comp = exec_ctx.tabela_simbolos.obter("operação").valor.upper()
		if comp in ["AND","E","&","^"]: exp = '{} and {}'
		if comp in ["OR","OU","|","v"]: exp = '{} or {}'
		if comp in ["NAND","NE","!&","!^","~&","~^"]: exp = '1 + (-{} and -{})'
		if comp in ["NOR","NOU","!|","!v","~|","~v"]: exp = '1 + (-{} or -{})'
		if comp in ["XOR","XOU"]: exp = '{} ^ {}'
		if comp in ["XNOR","XNOU"]: exp = '1 + (-{} ^ -{})'
		if comp in ["CONDICIONAL","->","=>"]: exp = '1 if {} == 1 else 0'
		if comp in ["BICONDICIONAL","<->","<=>"]: exp = '1 + (-{} ^ -{})'

		if exp:
			for l in range(3,-1,-1):
				p1 = str(int(l/2))
				p2 = str(l%2)
				print(f"{p1} {comp} {p2} = {str(int(eval(exp.format(p1,p2))))}")
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_tabela_binario.arg_names = ["operação"]

	def executar_tabela_logico(self, exec_ctx):
		exp = None
		comp = exec_ctx.tabela_simbolos.obter("operação").valor.upper()
		if comp in ["AND","E","&","^"]: exp = '{} and {}'
		if comp in ["OR","OU","|","v"]: exp = '{} or {}'
		if comp in ["NAND","NE","!&","!^","~&","~^"]: exp = '1 + (-{} and -{})'
		if comp in ["NOR","NOU","!|","!v","~|","~v"]: exp = '1 + (-{} or -{})'
		if comp in ["XOR","XOU"]: exp = '{} ^ {}'
		if comp in ["XNOR","XNOU"]: exp = '1 + (-{} ^ -{})'
		if comp in ["CONDICIONAL","->","=>"]: exp = '1 if {} == 1 else 0'
		if comp in ["BICONDICIONAL","<->","<=>"]: exp = '1 + (-{} ^ -{})'

		if exp:
			for l in range(3,-1,-1):
				vl = ['F','V']
				p1 = int(l/2)
				p2 = l%2
				print(f"{vl[p1]} {comp} {vl[p2]} = {vl[int(eval(exp.format(p1,p2)))]}")
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_tabela_logico.arg_names = ["operação"]

	def executar_adicionar(self, exec_ctx):
		lista = exec_ctx.tabela_simbolos.obter("list")
		valor = exec_ctx.tabela_simbolos.obter("valor")

		if not isinstance(lista, Lista):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,EM_FirstArgList,exec_ctx))

		lista.elementos.append(valor)
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_adicionar.arg_names = ["list", "valor"]

	def executar_remover(self, exec_ctx):
		lista = exec_ctx.tabela_simbolos.obter("list")
		index = exec_ctx.tabela_simbolos.obter("index")

		if not isinstance(lista, Lista): return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,EM_FirstArgList,exec_ctx))
		if not isinstance(index, Numero): return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,EM_SecoArgNum,exec_ctx))

		try:
			element = lista.elementos.pop(index.valor)
		except:
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,EM_ListBounds,exec_ctx))
		return ResultadoDaRT().sucesso(element)
	executar_remover.arg_names = ["list", "index"]

	def executar_extender(self, exec_ctx):
		listA = exec_ctx.tabela_simbolos.obter("listA")
		listB = exec_ctx.tabela_simbolos.obter("listB")

		if not isinstance(listA, Lista):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,EM_FirstArgList,exec_ctx))

		if not isinstance(listB, Lista):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,EM_SecoArgList,exec_ctx))

		listA.elementos.extend(listB.elementos)
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_extender.arg_names = ["listA", "listB"]

	def executar_tamanho(self, exec_ctx):
		lista = exec_ctx.tabela_simbolos.obter("lista")

		if not isinstance(lista, Lista):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,EM_FirstArgList,exec_ctx))
		return ResultadoDaRT().sucesso(Numero(len(lista.elementos)))
	executar_tamanho.arg_names = ["list"]

	def executar_obter_hora_atual(self, exec_ctx):
		d = datetime.datetime.today().strftime("%H:%M:%S")
		return ResultadoDaRT().sucesso(Texto(d))
	executar_obter_hora_atual.arg_names = []

	def executar_obter_data_atual(self, exec_ctx):
		d = datetime.datetime.today().strftime("%d/%m/%Y")
		return ResultadoDaRT().sucesso(Texto(d))
	executar_obter_data_atual.arg_names = []

	def executar_abrir(self, exec_ctx):
		arquivo = exec_ctx.tabela_simbolos.obter("arquivo")

		if not isinstance(arquivo, Texto):
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,EM_FirstArgPath,exec_ctx))

		arquivo = arquivo.valor

		try:
			with open(arquivo, "r") as f: script = f.read()
		except Exception as e:
			return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,EM_ScriptLoad.format(arquivo) + "\n" + str(e),exec_ctx))
		_, erro = executar(arquivo, script)
		
		if erro: return ResultadoDaRT().falha(ErroRT(self.inicio, self.fim,EM_ScriptFinish.format(arquivo) + "\n" + erro.como_texto(),exec_ctx))
		return ResultadoDaRT().sucesso(Numero.nulo)
	executar_abrir.arg_names = ["arquivo"]

#CRIAR FUNÇÃO INSTALADA PARA CADA NOME E INSTRUÇÃO
for i in (
	('listar',''),
	('escrever','texto'),
	('escrever_ret','texto'),
	('ler',''),
	('ler_inteiro',''),
	('limpar',''),
	('pausar',''),
	('esperar','segundos'),
	('e_um_numero','variável'),
	('e_um_texto','variável'),
	('e_uma_lista','variável'),
	('e_uma_funcao','variável'),
	('tabela_binario',''),
	('tabela_logico',''),
	('adicionar','variável'),
	('remover','variável'),
	('extender','tamanho'),
	('tamanho','lista'),
	('obter_hora_atual',''),
	('obter_data_atual',''),
	('abrir','arquivo')):
	exec(f'FuncaoInstalada.{i[0]} = FuncaoInstalada("{i[0]}","{i[1]}")')
