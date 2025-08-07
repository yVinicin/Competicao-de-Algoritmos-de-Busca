# Alunos:
#   Equipe 1: Gabriel Pereira e Gabriel Neneve
#   Equipe 2: Thalita e Vinícius Mattos
# Disciplina: Inteligência Artificial - Profª Adriana Postal
# Problema: Jogo da Velha - Competição de Algoritmos
# Algoritmos: Minimax com Tabela de Transposição (MTT) e Alpha-Beta Pruning

import pygame
import time

from JogoDaVelha import JogoDaVelha
from JogadorIA import MTT, JogadorAlphaBeta
from Interface import Interface

def processar_eventos():
    # Processa eventos do Pygame, retorna False se o usuário fechar a janela
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
    return True

def executar_jogada(jogo, jogador_atual, ia1, ia2, tempos_ia1, tempos_ia2):
    #Agora a letra certa é atribuida a cada partida, em vez de assumir que ia1 é sempre 'X'.
    
    inicio = time.time()
    if ia1.letra == jogador_atual:
        jogada = ia1.escolher_jogada(jogo)
        tempos_ia1.append(time.time() - inicio)
        print(f"Jogada IA 1 ({ia1.letra}): {jogada}, Nós explorados: {ia1.nos_explorados}")
    elif ia2.letra == jogador_atual:
        jogada = ia2.escolher_jogada(jogo)
        tempos_ia2.append(time.time() - inicio)
        print(f"Jogada IA 2 ({ia2.letra}): {jogada}, Nós explorados: {ia2.nos_explorados}")
    return jogada

def main():
    # Inicializa o Pygame e configura a janela
    pygame.init()
    pausado = False
    tela = pygame.display.set_mode((1500, 800))
    pygame.display.set_caption("Jogo da Velha - IA vs IA")
    interface = Interface(tela)
    relogio = pygame.time.Clock()

    # Estatísticas do jogo
    vitorias_jogador1 = 0
    vitorias_jogador2 = 0
    empates = 0
    partidas = 0
    max_partidas = 20

    jogo = JogoDaVelha()

    ia1 = MTT('X')
    ia2 = JogadorAlphaBeta('O')

    jogador_atual = 'X'
    jogador1_letra = 'X'
    jogador2_letra = 'O'

    tempos_ia1 = []
    tempos_ia2 = []

    rodando = True
    jogando_partida = True
    partidas = 0

    while rodando:
        # Desenha o tabuleiro e as jogadas
        interface.desenhar_tabuleiro()
        interface.desenhar_jogadas(jogo.tabuleiro)
        # Calcula tempos médios das IAs
        tempo_medio_ia1 = sum(tempos_ia1) / len(tempos_ia1) if len(tempos_ia1) > 0 else 0.0
        tempo_medio_ia2 = sum(tempos_ia2) / len(tempos_ia2) if len(tempos_ia2) > 0 else 0.0
        # Exibe pontuação, tempos e botão de pausa
        interface.exibir_pontuacao(vitorias_jogador1, vitorias_jogador2, empates, tempo_medio_ia1, tempo_medio_ia2)
        botao_pause_rect = interface.botao_pause(pausado)
        if pausado:
            interface.exibir_status_pausa()
        pygame.display.flip()
        relogio.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_pause_rect.collidepoint(event.pos):
                    pausado = not pausado  # Alterna pausa


        if jogando_partida and not pausado:
            # Executa a jogada da IA atual
            jogada = executar_jogada(jogo, jogador_atual, ia1, ia2, tempos_ia1, tempos_ia2)

            if jogo.fazer_jogada(jogada, jogador_atual):
                time.sleep(0.4)  # Delay para visualização da jogada
                if jogo.vencedor_atual:
                    if jogador_atual == jogador1_letra:
                        vitorias_jogador1 += 1
                    else:
                        vitorias_jogador2 += 1
                    jogando_partida = False
                elif not jogo.tem_espaco_vazio():
                    empates += 1
                    jogando_partida = False
                else:
                    # Alterna jogador
                    jogador_atual = jogador2_letra if jogador_atual == jogador1_letra else jogador1_letra

        elif not jogando_partida and not pausado:
            partidas += 1
            vencedor = 0
            if jogo.vencedor_atual == jogador1_letra:
                vencedor = 1
            elif jogo.vencedor_atual == jogador2_letra:
                vencedor = 2

            # Remove a interação com o usuário para jogar novamente, tornando automático
            if partidas < max_partidas:
                jogador1_letra, jogador2_letra = jogador2_letra, jogador1_letra
                jogador_atual = jogador1_letra
                jogo.resetar()
                jogando_partida = True
            else:
                rodando = False

    pygame.quit()

    # Estatísticas finais no terminal
    print(f"Total de partidas: {partidas}")
    print(f"Jogador 1 (Minimax TT) venceu: {vitorias_jogador1}")
    print(f"Jogador 2 (AlphaBeta) venceu: {vitorias_jogador2}")
    print(f"Empates: {empates}")
    if tempos_ia1:
        print(f"Tempo médio por jogada IA 1: {sum(tempos_ia1)/len(tempos_ia1):.4f} segundos")
    if tempos_ia2:
        print(f"Tempo médio por jogada IA 2: {sum(tempos_ia2)/len(tempos_ia2):.4f} segundos")

if __name__ == "__main__":
    main()
