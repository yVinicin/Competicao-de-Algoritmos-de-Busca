# Alunos:
#   Equipe 1: Gabriel Pereira e Gabriel Neneve
#   Equipe 2: Thalita e Vinícius Mattos
# Disciplina: Inteligência Artificial - Profª Adriana Postal
# Problema: Jogo da Velha - Competição de Algoritmos
# Algoritmos: Minimax com Tabela de Transposição (MTT) e Alpha-Beta Pruning

import math
import random

def avaliacao_tabuleiro(estado, jogador):
    pontos = 0
    oponente = 'O' if jogador == 'X' else 'X'

    # Define todas as linhas de vitória (linhas, colunas, diagonais)
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]             # Diagonais
    ]

    for line in winning_lines:
        contagem_jogador = 0
        contagem_oponente = 0
        empty_count = 0
        for i in line:
            if estado.tabuleiro[i] == jogador:
                contagem_jogador += 1
            elif estado.tabuleiro[i] == oponente:
                contagem_oponente += 1
            else:
                empty_count += 1

        # Pontuação baseada em linhas potenciais
        if contagem_jogador == 3:
            pontos += 1000  # Vitória imediata
        elif contagem_jogador == 2 and empty_count == 1:
            pontos += 100   # Quase vitória
        elif contagem_jogador == 1 and empty_count == 2:
            pontos += 10    # Uma peça na linha

        if contagem_oponente == 3:
            pontos -= 1000  # Derrota imediata
        elif contagem_oponente == 2 and empty_count == 1:
            pontos -= 100   # Oponente quase vitória (precisa bloquear)
        elif contagem_oponente == 1 and empty_count == 2:
            pontos -= 10    # Oponente com uma peça na linha

    # Priorizar o centro
    if estado.tabuleiro[4] == jogador:
        pontos += 50
    elif estado.tabuleiro[4] == oponente:
        pontos -= 50

    # Priorizar cantos
    for cantos in [0, 2, 6, 8]:
        if estado.tabuleiro[cantos] == jogador:
            pontos += 20
        elif estado.tabuleiro[cantos] == oponente:
            pontos -= 20

    return pontos

class MTT:
    def __init__(self, letra):
        self.letra = letra
        self.transposicao = {}
        self.nos_explorados = 0

    @property
    def oponente(self):
        return 'O' if self.letra == 'X' else 'X'

    def escolher_jogada(self, jogo):
        self.nos_explorados = 0
        self.transposicao.clear()
        jogadas_disponiveis = jogo.jogadas_disponiveis()
        if len(jogadas_disponiveis) == 9:
            # Preferir um canto no início
            cantos = [0, 2, 6, 8]
            return random.choice(cantos)
        else:
            pontuacao, jogada = self.minimax(jogo, self.letra)
            return jogada

    def estado_hash(self, estado):
        return ''.join(estado.tabuleiro)

    def minimax(self, estado, jogador, profundidade=0):
        self.nos_explorados += 1
        chave = self.estado_hash(estado)
        if chave in self.transposicao:
            return self.transposicao[chave]

        if estado.vencedor_atual == self.letra:
            return (10 - profundidade, None)
        elif estado.vencedor_atual == self.oponente:
            return (-10 + profundidade, None)
        elif not estado.tem_espaco_vazio():
            return (0, None)

        if jogador == self.letra:
            melhor_pontuacao = -math.inf
            melhor_movimento = None
            for movimento in estado.jogadas_disponiveis():
                vencedor_antes_jogada = estado.vencedor_atual
                estado.fazer_jogada(movimento, jogador)
                pontuacao, _ = self.minimax(estado, self.oponente, profundidade + 1)
                estado.desfazer_jogada(movimento)
                estado.vencedor_atual = vencedor_antes_jogada

                if pontuacao > melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_movimento = movimento
        else:
            melhor_pontuacao = math.inf
            melhor_movimento = None
            for movimento in estado.jogadas_disponiveis():
                vencedor_antes_jogada = estado.vencedor_atual
                estado.fazer_jogada(movimento, jogador)
                pontuacao, _ = self.minimax(estado, self.letra, profundidade + 1)
                estado.desfazer_jogada(movimento)
                estado.vencedor_atual = vencedor_antes_jogada

                if pontuacao < melhor_pontuacao:
                    melhor_pontuacao = pontuacao
                    melhor_movimento = movimento

        self.transposicao[chave] = (melhor_pontuacao, melhor_movimento)
        return self.transposicao[chave]

class JogadorAlphaBeta:
    def __init__(self, letra):
        self.letra = letra
        self.nos_explorados = 0

    @property
    def oponente(self):
        #Oponente é uma propriedade dinâmica, para garantir que seja sempre o oposto de self.letra
        return 'O' if self.letra == 'X' else 'X'

    def escolher_jogada(self, jogo):
        self.nos_explorados = 0
        jogadas_disponiveis = jogo.jogadas_disponiveis()
        if len(jogadas_disponiveis) == 9:
            return 4

        melhor_pontuacao = -math.inf
        melhor_jogada = None

        for movimento in jogadas_disponiveis:
            jogo.fazer_jogada(movimento, self.letra)
            profundidade = len(jogo.jogadas_disponiveis())
            pontuacao, _ = self.alphabeta(jogo, profundidade, -math.inf, math.inf, False)
            jogo.desfazer_jogada(movimento)
            jogo.vencedor_atual = None

            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_jogada = movimento
        
        return melhor_jogada

    def alphabeta(self, estado, profundidade, alpha, beta, maximizando_jogador):
        self.nos_explorados += 1

        if estado.vencedor_atual:
            return (1000 * (profundidade + 1), None) if estado.vencedor_atual == self.letra else (-1000 * (profundidade + 1), None)
        elif not estado.tem_espaco_vazio() or profundidade == 0:
            return (avaliacao_tabuleiro(estado, self.letra), None)

        if maximizando_jogador:
            melhor_valor = -math.inf
            for movimento in estado.jogadas_disponiveis():
                estado.fazer_jogada(movimento, self.letra)
                pontuacao, _ = self.alphabeta(estado, profundidade - 1, alpha, beta, False)
                estado.desfazer_jogada(movimento)
                estado.vencedor_atual = None
                
                melhor_valor = max(melhor_valor, pontuacao)
                alpha = max(alpha, melhor_valor)
                if beta <= alpha:
                    break
            return melhor_valor, None
        else:
            melhor_valor = math.inf
            for movimento in estado.jogadas_disponiveis():
                estado.fazer_jogada(movimento, self.oponente)
                pontuacao, _ = self.alphabeta(estado, profundidade - 1, alpha, beta, True)
                estado.desfazer_jogada(movimento)
                estado.vencedor_atual = None
                
                melhor_valor = min(melhor_valor, pontuacao)
                beta = min(beta, melhor_valor)
                if beta <= alpha:
                    break
            return melhor_valor, None
