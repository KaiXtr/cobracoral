import cobracoral

print('$$$ $$$ $$$ $$$ $$$ $$$ $$$ $$$ $$$ $  ')
print('$   $ $ $ $ $ $ $ $ $   $ $ $ $ $ $ $  ')
print('$   $ $ $$  $$  $$$ $   $ $ $$  $$$ $  ')
print('$   $ $ $ $ $ $ $ $ $   $ $ $ $ $ $ $  ')
print('$$$ $$$ $$$ $ $ $ $ $$$ $$$ $ $ $ $ $$$')
print('Desenvolvida por Ewerton Matheus Bezerra Ramos\n')

while True:
    texto = input('{{ ')
    if texto.strip() == "": continue
    
    resultado, erro = cobracoral.executar('<stdin>', texto)

    if erro: print(erro.como_texto())
    elif resultado:
    	if len(resultado.elementos) == 1: print(repr(resultado.elementos[0]))
    	else: print(repr(resultado))