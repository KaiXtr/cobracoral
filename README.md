# Cobracoral
 Linguagem de programação feita para ensinar algoritmos.
 Portugol programming language for learning

# Como programar em Cobracoral:

## Variáveis
Formados por um par **_nome da variável_ = _valor da variável_**, são todos os dados necessários para a execução e criação de um algoritmo. As variáveis podem conter valores de vários tipos, como _inteiro, texto, lógico e real_.
    `var x = 10`<br>
    `var y = "Olá Mundo!"`<br>
    `var z = verdadeiro`<br>
    `var a = 2.5`<br>
    `var b = pi`<br>

## Comentários
Comentários são trechos do código que não são processados pelo interpretador, sendo livres para escrita fora da programação.
    `# comentário`<br>
    `# eu posso escrever o que eu quiser aqui`<br>

## Aritmética
**Adição:**<br>
    `x mais y`<br>
    `x + y`<br>
**Subtração:**<br>
    `x menos y`<br>
    `x - y`<br>
**Multiplicação:**<br>
    `x vezes y`<br>
    `x * y`<br>
    `x × y`<br>
**Divisão:**<br>
    `x dividido y`<br>
    `x / y`<br>
    `x \ y`<br>
    `x ÷ y`<br>
**Resto da divisão:**<br>
    `x resto y`<br>
    `x % y`<br>
**Potenciação:**<br>
    `x elevado y`<br>
    `x ^ y`<br>
    `x ** y`<br>
**Radiciação:**<br>
    `x rad y`<br>
    `x √ y`<br>
    `x // y`<br>

## Comparações Numéricas
**Igualdade:**<br>
    `0 == 0 ∴ verdadeiro`<br>
    `0 == 1 ∴ falso`<br>
**Diferença:**<br>
    `0 != 0 ∴ falso`<br>
    `0 != 1 ∴ verdadeiro`<br>
    `0 ~= 0 ∴ falso`<br>
    `0 ~= 1 ∴ verdadeiro`<br>
**Menor que:**<br>
    `2 < 3 ∴ verdadeiro`<br>
    `3 < 2 ∴ falso`<br>
**Maior que**<br>
    `2 > 3 ∴ falso`<br>
    `3 > 2 ∴ verdadeiro`<br>
**Menor ou igual a:**<br>
    `2 <= 2 ∴ verdadeiro`<br>
    `1 <= 2 ∴ verdadeiro`<br>
    `3 >= 2 ∴ falso`<br>
**Maior ou igual a:**<br>
    `6 >= 6 ∴ verdadeiro`<br>
    `8 >= 6 ∴ verdadeiro`<br>
    `3 >= 6 ∴ falso`<br>

## Comparações Lógicas
**AND:**<br>
    `1 e 1 ∴ verdadeiro`<br>
    `0 e 1 ∴ falso`<br>
    `1 & 0 ∴ falso`<br>
    `0 & 0 ∴ falso`<br>
**OR:**<br>
    `1 ou 1 ∴ verdadeiro`<br>
    `0 ou 1 ∴ verdadeiro`<br>
    `1 | 0 ∴ verdadeiro`<br>
    `0 | 0 ∴ falso`<br>
**NAND:**<br>
    `1 ne 1 ∴ falso`<br>
    `0 ne 1 ∴ verdadeiro`<br>
    `1 !& 0 ∴ verdadeiro`<br>
    `0 ~& 0 ∴ verdadeiro`<br>
**NOR:**<br>
    `1 nou 1 ∴ falso`<br>
    `0 nou 1 ∴ falso`<br>
    `1 !| 0 ∴ falso`<br>
    `0 ~| 0 ∴ verdadeiro`<br>
**XOR:**<br>
    `1 xou 1 ∴ falso`<br>
    `0 xou 1 ∴ verdadeiro`<br>
    `1 xou 0 ∴ verdadeiro`<br>
    `0 xou 0 ∴ falso`<br>
**XNOR:**<br>
    `1 xnou 1 ∴ verdadeiro`<br>
    `0 xnou 1 ∴ falso`<br>
    `1 xnou 0 ∴ falso`<br>
    `0 xnou 0 ∴ verdadeiro`<br>
**Condicional:**<br>
    `1 => 1 ∴ verdadeiro`<br>
    `0 => 1 ∴ falso`<br>
    `1 => 0 ∴ verdadeiro`<br>
    `0 => 0 ∴ verdadeiro`<br>
**Bicondicional:**<br>
    `1 <=> 1 ∴ verdadeiro`<br>
    `0 <=> 1 ∴ falso`<br>
    `1 <=> 0 ∴ falso`<br>
    `0 <=> 0 ∴ verdadeiro`<br>

## Entrada e Saída de Dados
**Comando _Escrever (texto)_:** escreve uma mensagem de texto no terminal.<br>
    `escrever("Olá Mundo!")`<br>
**Comando _Escrever_ret (texto)_:** escreve uma mensagem de texto no terminal e retorna o resultado.<br>
    `escrever_ret("Olá Mundo!")`<br>
**Comando _Ler (variável)_:** aguarda a entrada de um usuário.<br>
    `ler(x)`<br>
**Comando _Ler_inteiro (variável)_:** aguarda a entrada de um número inteiro do usuário.<br>
    `ler_inteiro(x)`<br>
**Comando _Limpar_:** limpa todo texto anterior do terminal.<br>
    `limpar()`<br>
    `cls()`<br>
**Comando _Pausar_ ()_:** aguarda uma tecla pressionada qualquer do usuário.<br>
    `pausar()`<br>
**Comando _Esperar (segundos)_:** espera por um intervalo de x segundos.<br>
    `esperar(3)`<br>

# Análise de dados
**Comando _É_um_número (variável)_:** verifica se a variável informada é um número.<br>
    `É_um_número(x)`<br>
    `E_um_número(x)`<br>
    `É_um_numero(x)`<br>
    `E_um_numero(x)`<br>
**Comando _É_um_número (variável)_:** verifica se a variável informada é um número.<br>
    `É_um_número(x)`<br>
    `E_um_número(x)`<br>
    `É_um_numero(x)`<br>
    `E_um_numero(x)`<br>

## Listas
**Comando _Adicionar (elemento)_:** adiciona um elemento à uma lista.<br>
    `x = [0,1]`<br>
    `x.adicionar(2)`<br>
    `x = [0,1,2]`<br>
**Comando _Remover (índice)_:** remove um elemento de uma lista.<br>
    `x = [2,5]`<br>
    `x.remover(1)`<br>
    `x = [2]`<br>
**Comando _Tamanho (lista/texto)_:** verifica o tamanho de uma lista ou texto.<br>
    `x = [0,1,5,8]`<br>
    `y = tamanho(x)`<br>
    `y = 4`<br>

## Funções gerais do Cobracoral
**Comando _Ajuda ()_:** exibe um texto de ajuda para o usuário.<br>
    `ajuda()`<br>
**Comando _Listar ()_:** exibe todas as funções instaladas da linguagem.<br>
    `lista()`<br>
**Comando _Sair ()_:** sair do shell da linguagem.<br>
    `sair()`<br>
    

# Agradecimentos
Muito obrigado, David Callanan, por disponibilizar o vídeo aulas sobre a criação de linguagens de programação e seu código fonte.
[Repositório]: (https://github.com/davidcallanan/py-myopl-code)