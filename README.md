# Cobracoral
 Linguagem de programação feita para ensinar algoritmos.
 Portugol programming language for learning

# Como programar em Cobracoral:

## Variáveis
Formados por um par **_nome da variável_ = _valor da variável_**, são todos os dados necessários para a execução e criação de um algoritmo. As variáveis podem conter valores de vários tipos, como _inteiro, texto, lógico e real_.
    `inteiro x = 10`
    `texto y = "Olá Mundo!"`
    `lógico z = verdadeiro`
    `real a = 2.5`
    `real b = pi`

## Comentários
Comentários são trechos do código que não são processados pelo interpretador, sendo livres para escrita fora da programação.
`# comentário`
`# eu posso escrever o que eu quiser aqui`

## Aritmética
**Adição:**
`x mais y`
`x + y`
**Subtração:**
`x menos y`
`x - y`
**Multiplicação:**
`x vezes y`
`x * y`
`x × y`
**Divisão:**
`x dividido y`
`x / y`
`x \ y`
`x ÷ y`
**Resto da divisão:**
`x resto y`
`x % y`
**Potenciação:**
`x elevado y`
`x ^ y`
`x ** y`
**Radiciação:**
`x rad y`
`x √ y`
`x // y`

## Comparações Numéricas
**Igualdade:**
`0 == 0 ∴ verdadeiro`
`0 == 1 ∴ falso`
**Diferença:**
`0 != 0 ∴ falso`
`0 != 1 ∴ verdadeiro`
`0 ~= 0 ∴ falso`
`0 ~= 1 ∴ verdadeiro`
**Menor que:**
`2 < 3 ∴ verdadeiro`
`3 < 2 ∴ falso`
**Maior que**
`2 > 3 ∴ falso`
`3 > 2 ∴ verdadeiro`
**Menor ou igual a:**
`2 <= 2 ∴ verdadeiro`
`1 <= 2 ∴ verdadeiro`
`3 >= 2 ∴ falso`
**Maior ou igual a:**
`6 >= 6 ∴ verdadeiro`
`8 >= 6 ∴ verdadeiro`
`3 >= 6 ∴ falso`

## Comparações Lógicas
**AND:**
`1 e 1 ∴ verdadeiro`
`0 e 1 ∴ falso`
`1 & 0 ∴ falso`
`0 & 0 ∴ falso`
**OR:**
`1 ou 1 ∴ verdadeiro`
`0 ou 1 ∴ verdadeiro`
`1 | 0 ∴ verdadeiro`
`0 | 0 ∴ falso`
**NAND:**
`1 ne 1 ∴ falso`
`0 ne 1 ∴ verdadeiro`
`1 !& 0 ∴ verdadeiro`
`0 ~& 0 ∴ verdadeiro`
**NOR:**
`1 nou 1 ∴ falso`
`0 nou 1 ∴ falso`
`1 !| 0 ∴ falso`
`0 ~| 0 ∴ verdadeiro`
**XOR:**
`1 xou 1 ∴ falso`
`0 xou 1 ∴ verdadeiro`
`1 xou 0 ∴ verdadeiro`
`0 xou 0 ∴ falso`
**XNOR:**
`1 xnou 1 ∴ verdadeiro`
`0 xnou 1 ∴ falso`
`1 xnou 0 ∴ falso`
`0 xnou 0 ∴ verdadeiro`
**Condicional:**
`1 => 1 ∴ verdadeiro`
`0 => 1 ∴ falso`
`1 => 0 ∴ verdadeiro`
`0 => 0 ∴ verdadeiro`
**Bicondicional:**
`1 <=> 1 ∴ verdadeiro`
`0 <=> 1 ∴ falso`
`1 <=> 0 ∴ falso`
`0 <=> 0 ∴ verdadeiro`

## Entrada e Saída de Dados
**Comando _Escrever (texto)_:** escreve uma mensagem de texto no terminal.
`escrever("Olá Mundo!")`
**Comando _Ler (variável)_:** aguarda a entrada de um usuário.
`ler(x)`

## Listas
**Comando _Limpar_:** limpa todo texto anterior do terminal.
`limpar()`
`cls()`
**Comando _Adicionar (elemento)_:** adiciona um elemento à uma lista.
`x = [0,1]`
`x.adicionar(2)`
`x = [0,1,2]`
**Comando _Remover (índice)_:** remove um elemento de uma lista.
`x = [2,5]`
`x.remover(1)`
`x = [2]`
**Comando _Tamanho (lista/texto)_:** verifica o tamanho de uma lista ou texto.
`x = [0,1,5,8]`
`y = tamanho(x)`
`y = 4`
    

# Agradecimentos
Muito obrigado, David Callanan, por disponibilizar o vídeo aulas sobre a criação de linguagens de programação e seu código fonte.
[Repositório]: (https://github.com/davidcallanan/py-myopl-code)