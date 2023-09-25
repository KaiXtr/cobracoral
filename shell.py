# -*- coding: utf-8 -*-
import cobracoral
import sys
import os

print('___█████_█████_█████_█████_█████_█████_█████_█████_█████_█_______')
print('___█_____█___█_█___█_█___█_█___█_█_____█___█_█___█_█___█_█_______')
print('___█_____█___█_████__████__█████_█_____█___█_████__█████_█_______')
print('___█_____█___█_█___█_█___█_█___█_█_____█___█_█___█_█___█_█_______')
print('___█████_█████_█████_█___█_█___█_█████_█████_█___█_█___█_█████___')
print('Desenvolvida por Ewerton Matheus Bezerra Ramos\n')

try:
	historico = [""]

	#EXECUTAR NO CONSOLE
	if len(sys.argv) == 1:
		console_texto = ":> "
		retornar_resultado = False

		while True:
			#LER COMANDO E ADICIONAR AO HISTÓRICO
			texto = input(console_texto)
			if texto.strip() == "": continue
			else: historico.append(texto)

			#AJUDA
			if texto.lower() == 'ajuda()':
				arq = open("ajuda.txt","r")
				print(arq.read())
				arq.close()
				print()
			
			#CONFIGURAÇÕES & MAIS
			elif texto.lower() == 'sair()': break
			elif texto.lower() in ('console_versão','console_versao'):
				print(f"cobracoral v.0.1 x64 - python {str(sys.version_info[0])}.{str(sys.version_info[1])}.{str(sys.version_info[2])}\n")
			elif texto.lower().startswith('console_texto ='):
				console_texto = texto[16:] + ' '
			elif texto.lower().startswith('retornar_resultado'):
				retornar_resultado = not retornar_resultado
			
			#INTERPRETAR CÓDIGO
			else:
				resultado, erro = cobracoral.executar('<stdin>', texto)
				if erro:
					print(f"{erro.como_texto()}\n")
				elif retornar_resultado and resultado:
					if len(resultado.elementos) == 1:
						print(f"= {repr(resultado.elementos[0])}\n")
					else:
						print(f"= {repr(resultado)}\n")

	#EXECUTAR ARQUIVO
	elif len(sys.argv) > 1:
		if sys.argv[1].endswith(".cc") or sys.argv[1].endswith(".cobracoral"):
			script = None
			try:
				with open(sys.argv[1], "r") as f: 
					cript = f.read()  
				resultado, erro = cobracoral.executar(sys.argv[1], script)
				if erro:
					print(erro.como_texto())
				'''elif resultado:
					if len(resultado.elementos) == 1: print('= ' + repr(resultado.elementos[0]))
					else: print('= ' + repr(resultado))'''
			except: print(f"Falha ao abrir o arquivo \"{sys.argv[1]}\" (talvez tenha sido deletado, movido ou renomeado)")
		else:
			os.system('cls' if os.name == 'nt' else 'clear')
			print("FORMATO INVÁLIDO DE ARQUIVO. Cobracoral executa apenas arquivos .cobracoral ou .cc")

	print("\nFim do programa.")

#FALHA NO CÓDIGO
except Exception:
	from traceback import extract_tb
	et, ev, eb = sys.exc_info()
	print('ESSA NÃO! COBRACORAL NÃO ESTÁ FUNCIONANDO!')
	for i in extract_tb(eb): print(f"	Arquivo {str(i[0])}, linha {str(i[1])} em {str(i[2])}:\n\t{str(i[3])}\n")
	print(f"{str(et.__name__)}: {str(ev)}")
	input()