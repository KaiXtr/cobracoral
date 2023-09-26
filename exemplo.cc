
escrever("QUIZ!")
pausar()
escrever("Qual conta está correta?")
esperar(1)
escrever("1: 75 + 25 = 100")
esperar(1)
escrever("2: 30 - 11 = 21")
esperar(1)
escrever("3: 45 - 3 = 41")

var x = ler_inteiro()

SE x == 1 ENTAO escrever("Certa resposta!") SENAO escrever("Você errou...")