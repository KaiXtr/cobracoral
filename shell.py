import cobracoral
import sys
import os

print('___█████.█████.█████.█████.█████.█████.█████.█████.█████.█....___')
print('___█.....█...█.█...█.█...█.█...█.█.....█...█.█...█.█...█.█....___')
print('___█.....█...█.████..████..█████.█.....█...█.████..█████.█....___')
print('___█.....█...█.█...█.█...█.█...█.█.....█...█.█...█.█...█.█....___')
print('___█████.█████.█████.█...█.█...█.█████.█████.█...█.█...█.█████___')
print('Desenvolvida por Ewerton Matheus Bezerra Ramos\n')

#EXECUTAR NO CONSOLE
if len(sys.argv) == 1:
	console_texto = "> "
	while True:
		texto = input(console_texto)
		if texto.strip() == "": continue
		
		#CONFIGURAÇÕES & MAIS
		elif texto.lower() == 'sair': break
		elif texto == 'CONSOLE_VERSÃO':
			print('cobracoral v.0.1 x64 - python ' + str(sys.version_info[0]) + '.' + str(sys.version_info[1]) + '.' + str(sys.version_info[2]))
		elif texto.startswith('CONSOLE_TEXTO ='):
			console_texto = texto[16:] + ' '
		
		#INTERPRETAR CÓDIGO
		else:
			resultado, erro = cobracoral.executar('<stdin>', texto)
			if erro: print(erro.como_texto())
			elif resultado:
				if len(resultado.elementos) == 1: print('= ' + repr(resultado.elementos[0]))
				else: print('= ' + repr(resultado))
		print()

#EXECUTAR ARQUIVO
elif len(sys.argv) > 1:
	if sys.argv[1].endswith('.cc') or sys.argv[1].endswith('.cobracoral'):
		script = None
		try:
			with open(sys.argv[1], "r") as f: script = f.read()  
			resultado, erro = cobracoral.executar(sys.argv[1], script)
			if erro: print(erro.como_texto())
			'''elif resultado:
				if len(resultado.elementos) == 1: print('= ' + repr(resultado.elementos[0]))
				else: print('= ' + repr(resultado))'''
		except: print(f"Falha ao abrir o arquivo \"{sys.argv[1]}\" (talvez tenha sido deletado, movido ou renomeado)")
	else:
		os.system('cls' if os.name == 'nt' else 'clear')
		print("FORMATO INVÁLIDO DE ARQUIVO. Cobracoral executa apenas arquivos .cobracoral ou .cc")

print("\nFim do programa.")