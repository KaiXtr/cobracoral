# -*- coding: utf-8 -*-
def listar_variacoes(texto):
	lista = [texto]
	old = None
	if True:
		for c in range(len(texto)):	
			for i in ACENTOS.items():
				if texto[c].lower() in i[1]:
					old = texto.replace(texto[c],i[0].upper())
					lista.append(old)
		texto = old if old else None
	return lista


ALFABETO = 'abcdefghijklmnopqrstuvwxyz'
ACENTOS = {'a': 'äåæªáâãà','c': 'ç','e': 'éèê','i': 'íìî','n': 'ñ','o': 'óòôõ','u': 'úù'}
ALFABETO += ''.join(ACENTOS.values()) + ''.join(ACENTOS.values()).upper() + ALFABETO.upper()
DIGITOS = '0123456789'
ALFANUMERICO = ALFABETO + DIGITOS

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

TT_INTCONJ	 = 'INTERSEÇÃO'
TT_DENCONJ	 = 'PERTENCE A'
TT_FORCONJ	 = 'NÃO PERTENCE A'

TT_ABRPARENT	= 'ABRE PARÊNTESES'
TT_FECPARENT	= 'FECHA PARÊNTESES'
TT_ABRCOLCHE	= 'ABRE COLCHETES'
TT_FECCOLCHE	= 'FECHA COLCHETES'
TT_ABRCHAVES	= 'ABRE CHAVES'
TT_FECCHAVES	= 'FECHA CHAVES'

TT_OPERAÇÕES = {
	'MAIS': TT_MAI,'MENOS': TT_MEN,'VEZES': TT_MUL,'DIVIDIDO': TT_DIV,'RESTO': TT_RES,'ELEVADO': TT_POT,'RAÍZ': TT_RAD,'RAIZ': TT_RAD,
	'IGUAL': TT_IGU,'DIFERENTE': TT_DIF,'MAIOR': TT_MIQ,'MENOR': TT_MNQ,
	'INTERSEÇÃO': TT_INTCONJ,'INTERSEÇAO': TT_INTCONJ,'INTERSECÃO': TT_INTCONJ,'INTERSECAO': TT_INTCONJ,
	'PERTENCE': TT_DENCONJ,'NÃOPERTENCE': TT_FORCONJ,'NAOPERTENCE': TT_FORCONJ,'DENTRO': TT_DENCONJ,'FORA': TT_FORCONJ
}

TT_PALAVRASCHAVE = [
	'VAR','E','OU','NE','NOU','XOU','XNOU','=>','<=>','NÃO','NAO','SE','SENÃOSE','SENAOSE','SENÃO','SENAO',
	'PARA','CADA','PASSO','ENQUANTO','FUNÇÃO','FUNCÃO','FUNÇAO','FUNCAO',
	'ENTÃO','ENTAO','FIM','RETORNAR','CONTINUAR','QUEBRAR'
]

PC_VAR = ('VAR','var')
PC_NAO = ('NÃO','NAO','não','nao')
PC_SE = ('SE','se')
PC_SENAOSE = ('SENÃOSE','SENAOSE','senãose','senaose')
PC_SENAO = ('SENÃO','SENAO','senão','senao')
PC_ENTAO = ('ENTÃO','ENTAO','então','entao')
PC_PARA = ('PARA','para')
PC_CADA = ('CADA','cada')
PC_PASSO = ('PASSO','passo')
PC_ENQUANTO = ('ENQUANTO','enquanto')
PC_FUNCAO = ('FUNÇÃO','FUNCÃO','FUNÇAO','FUNCAO','função','funcão','funçao','funcao')
PC_RETORNAR = ('RETORNAR','retornar')
PC_CONTINUAR = ('CONTINUAR','continuar')
PC_QUEBRAR = ('QUEBRAR','quebrar')
PC_FIM = ('FIM','fim')

TT_OPERAÇÕES = {**TT_OPERAÇÕES,**{i[0].lower(): i[1] for i in TT_OPERAÇÕES.items()}}
TT_PALAVRASCHAVE += [i.lower() for i in TT_PALAVRASCHAVE]

REPR_ANON = '<anônimo>'
REPR_FUNC = '<função {}>'
REPR_BUILTIN = '<função instalada {}>'

EM_FILE = 'Arquivo'
EM_LINE = 'linha'
EM_IN = 'em'
EM_OR = 'ou'
EM_AFTER = 'depois de'
EM_ZeroDiv = 'Você não sabe que é impossível dividir por zero??'
EM_IlegalOp = 'Operação Ilegal'
EM_IlegalChar = 'Este caractere não deveria estar aqui'
EM_ExpectedChar = 'Eu estava esperando outro caractere'
EM_Sintax = 'Esta linha não está bem estruturada'
EM_Runtime = 'Erro de processamento'
EM_Token = 'Token não pôde aparecer após tokens anteriores'
EM_Traceback = 'O caminho de volta: (última linha executada por último):'
EM_MustInt = 'O valor precisa ser um número do tipo inteiro!'
EM_Identifier = 'Esperava identificador'
EM_Expected = 'Estava esperando um '
EM_BuiltinFunc = 'Você não pode substituir uma função instalada!'
EM_Copy = 'Nenhum método de cópia definido.'
EM_ListBounds = 'Element at this index could not be removed from list because index is out of bounds'
EM_NoVar = 'Não existe nenhuma variável chamada "{}".'
EM_NoFunc = 'Nenhuma função "{}" foi definida.'
EM_FirstArgNum = 'O primeiro argumento precisa ser um número'
EM_SecoArgNum = 'O segundo argumento precisa ser um número'
EM_FirstArgList = 'O primeiro argumento precisa ser uma lista'
EM_SecoArgList = 'O segundo argumento precisa ser uma lista'
EM_FirstArgPath = 'O primeiro argumento precisa ser o caminho até o arquivo em texto'
EM_ArgsMuch = 'tem argumentos demais sendo passados para'
EM_ArgsFew = 'tem poucos argumentos sendo passados para'
EM_ScriptLoad = 'Falha ao carregar o arquivo "{}"'
EM_ScriptFinish = 'Falha ao terminar de executar o arquivo "{}"'