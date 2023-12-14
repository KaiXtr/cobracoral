# -*- coding: utf-8 -*-
#######################################
# CONSTANTES
#######################################

from keywords_PT import *
from erros import *
from posicao import *

import datetime
import time
import os

from tokens import *
from lexer import *
from nodes import *	
from cbr_parser import *
from resultado_da_rt import *
from valores import *
from funcoes import *
from contexto import *
from tabela_de_simbolos import *

#######################################
# EXECUTAR
#######################################

class Interpretador:
	def visitar(self, node, contexto):
		method_name = f'visitar_{type(node).__name__}'
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, contexto)

	def no_visit_method(self, node, contexto):
		raise Exception(EM_NoFunc.format("visitar_" + type(node).__name__))

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
		if not valor: return resultado.falha(ErroRT(node.inicio, node.fim,EM_NoVar.format(nome),contexto))
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
		elif node.tok_op.tipo == TT_RES: valor, erro = esquerdo.resto(direito)
		elif node.tok_op.tipo == TT_POT: valor, erro = esquerdo.elevado_a(direito)
		elif node.tok_op.tipo == TT_RAD: valor, erro = esquerdo.radiciacao(direito)
		elif node.tok_op.tipo == TT_EIG: valor, erro = esquerdo.comparar_igualdade(direito)
		elif node.tok_op.tipo == TT_DIF: valor, erro = esquerdo.comparar_diferenca(direito)
		elif node.tok_op.tipo == TT_MNQ: valor, erro = esquerdo.comparar_menor_que(direito)
		elif node.tok_op.tipo == TT_MIQ: valor, erro = esquerdo.comparar_maior_que(direito)
		elif node.tok_op.tipo == TT_MNQIGU: valor, erro = esquerdo.comparar_menor_igual_que(direito)
		elif node.tok_op.tipo == TT_MIQIGU: valor, erro = esquerdo.comparar_maior_igual_que(direito)
		elif node.tok_op.tipo == TT_INTCONJ: valor, erro = esquerdo.intersecao_de(direito)
		elif node.tok_op.tipo == TT_DENCONJ: valor, erro = esquerdo.pertence_a(direito)
		elif node.tok_op.tipo == TT_FORCONJ: valor, erro = esquerdo.nao_pertence_a(direito)
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
			if not condicao.e_verdade(): break

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

		if isinstance(fim,Lista): limite = len(fim.elementos)
		else: limite = fim.valor

		if passo.valor >= 0: condition = lambda: i < limite
		else: condition = lambda: i > limite
		
		while condition():
			if isinstance(fim,Lista): contexto.tabela_simbolos.criar(node.node_nome.valor, Numero(fim.elementos[i]))
			else: contexto.tabela_simbolos.criar(node.node_nome.valor, Numero(i))
			
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
		corpo = node.node_corpo
		argumentos = [arg.valor for arg in node.tokens_nomes]
		valor = Funcao(nome, corpo, argumentos, node.retornar_automaticamente).fazer_contexto(contexto).fazer_posicao(node.inicio, node.fim)
		
		if node.node_nome: contexto.tabela_simbolos.criar(nome, valor)

		return resultado.sucesso(valor)

	def visitar_NodeChamar(self, node, contexto):
		resultado = ResultadoDaRT()
		args = []

		valor = resultado.registro(self.visitar(node.node_chamado, contexto))
		if resultado.deve_retornar(): return resultado
		valor = valor.copia().fazer_posicao(node.inicio, node.fim)

		for argumento in node.nodes:
			args.append(resultado.registro(self.visitar(argumento, contexto)))
			if resultado.deve_retornar(): return resultado
		
		retornar_valor = resultado.registro(valor.executar(args))
		if resultado.deve_retornar(): return resultado
		retornar_valor = retornar_valor.copia().fazer_posicao(node.inicio, node.fim).fazer_contexto(contexto)
		return resultado.sucesso(retornar_valor)

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
	tabela_global_simbolos.criar(eval(f"'NULO'.{case}()"), Numero.nulo)
	tabela_global_simbolos.criar(eval(f"'FALSO'.{case}()"), Numero.falso)
	tabela_global_simbolos.criar(eval(f"'VERDADEIRO'.{case}()"), Numero.verdadeiro)
	tabela_global_simbolos.criar(eval(f"'PI'.{case}()"), Numero.pi)
	tabela_global_simbolos.criar(eval(f"'LISTAR'.{case}()"), FuncaoInstalada.listar)
	tabela_global_simbolos.criar(eval(f"'ESCREVER'.{case}()"), FuncaoInstalada.escrever)
	tabela_global_simbolos.criar(eval(f"'ESCREVER_RET'.{case}()"), FuncaoInstalada.escrever_ret)
	tabela_global_simbolos.criar(eval(f"'LER'.{case}()"), FuncaoInstalada.ler)
	tabela_global_simbolos.criar(eval(f"'LER_INTEIRO'.{case}()"), FuncaoInstalada.ler_inteiro)
	tabela_global_simbolos.criar(eval(f"'LIMPAR'.{case}()"), FuncaoInstalada.limpar)
	tabela_global_simbolos.criar(eval(f"'CLS'.{case}()"), FuncaoInstalada.limpar)
	tabela_global_simbolos.criar(eval(f"'PAUSAR'.{case}()"), FuncaoInstalada.pausar)
	tabela_global_simbolos.criar(eval(f"'ESPERAR'.{case}()"), FuncaoInstalada.esperar)
	tabela_global_simbolos.criar(eval(f"'E_UM_NUMERO'.{case}()"), FuncaoInstalada.e_um_numero)
	tabela_global_simbolos.criar(eval(f"'É_UM_NUMERO'.{case}()"), FuncaoInstalada.e_um_numero)
	tabela_global_simbolos.criar(eval(f"'E_UM_NÚMERO'.{case}()"), FuncaoInstalada.e_um_numero)
	tabela_global_simbolos.criar(eval(f"'É_UM_NÚMERO'.{case}()"), FuncaoInstalada.e_um_numero)
	tabela_global_simbolos.criar(eval(f"'É_UM_TEXTO'.{case}()"), FuncaoInstalada.e_um_texto)
	tabela_global_simbolos.criar(eval(f"'E_UM_TEXTO'.{case}()"), FuncaoInstalada.e_um_texto)
	tabela_global_simbolos.criar(eval(f"'É_UMA_LISTA'.{case}()"), FuncaoInstalada.e_uma_lista)
	tabela_global_simbolos.criar(eval(f"'E_UMA_LISTA'.{case}()"), FuncaoInstalada.e_uma_lista)
	tabela_global_simbolos.criar(eval(f"'É_UMA_FUNÇÃO'.{case}()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval(f"'E_UMA_FUNÇÃO'.{case}()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval(f"'E_UMA_FUNCÃO'.{case}()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval(f"'E_UMA_FUNCAO'.{case}()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval(f"'É_UMA_FUNCÃO'.{case}()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval(f"'E_UMA_FUNÇAO'.{case}()"), FuncaoInstalada.e_uma_funcao)
	tabela_global_simbolos.criar(eval(f"'TABELA_BINÁRIO'.{case}()"), FuncaoInstalada.tabela_binario)
	tabela_global_simbolos.criar(eval(f"'TABELA_BINARIO'.{case}()"), FuncaoInstalada.tabela_binario)
	tabela_global_simbolos.criar(eval(f"'TABELA_LÓGICO'.{case}()"), FuncaoInstalada.tabela_logico)
	tabela_global_simbolos.criar(eval(f"'TABELA_LOGICO'.{case}()"), FuncaoInstalada.tabela_logico)
	tabela_global_simbolos.criar(eval(f"'ADD'.{case}()"), FuncaoInstalada.adicionar)
	tabela_global_simbolos.criar(eval(f"'ADICIONAR'.{case}()"), FuncaoInstalada.adicionar)
	tabela_global_simbolos.criar(eval(f"'REMOVER'.{case}()"), FuncaoInstalada.remover)
	tabela_global_simbolos.criar(eval(f"'EXTENDER'.{case}()"), FuncaoInstalada.extender)
	tabela_global_simbolos.criar(eval(f"'TAMANHO'.{case}()"), FuncaoInstalada.tamanho)
	tabela_global_simbolos.criar(eval(f"'OBTER_HORA_ATUAL'.{case}()"), FuncaoInstalada.obter_hora_atual)
	tabela_global_simbolos.criar(eval(f"'OBTER_DATA_ATUAL'.{case}()"), FuncaoInstalada.obter_data_atual)
	tabela_global_simbolos.criar(eval(f"'ABRIR'.{case}()"), FuncaoInstalada.executar)

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