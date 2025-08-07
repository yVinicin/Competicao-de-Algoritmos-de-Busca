# Alunos:
#   Equipe 1: Gabriel Pereira e Gabriel Neneve
#   Equipe 2: Thalita e Vinícius Mattos
# Disciplina: Inteligência Artificial - Profª Adriana Postal
# Problema: Jogo da Velha - Competição de Algoritmos
# Algoritmos: Minimax com Tabela de Transposição (MTT) e Alpha-Beta Pruning

import pygame

# Cores
COR_FUNDO = pygame.Color("aquamarine4")
COR_TABULEIRO = pygame.Color("white")
COR_LINHAS = pygame.Color("black")
COR_X = pygame.Color("forestgreen")
COR_O = pygame.Color("midnightblue")
COR_TEXTO = pygame.Color("white")
COR_MODAL_FUNDO = pygame.Color("gray10")
COR_MODAL_BORDA = pygame.Color("white")
COR_BOTAO_JOGAR = pygame.Color("green")
COR_BOTAO_SAIR = pygame.Color("red")
COR_BOTAO_TEXTO = pygame.Color("white")

LARGURA_JANELA = 1500
ALTURA_JANELA = 800

# Inicializa a tela do jogo com as dimensões definidas
screen = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("Jogo da Velha - IA vs IA")

class Interface:
    def __init__(self, tela):
        # Inicializa a interface com a tela do Pygame
        self.tela = tela
        self.largura_tab = 600  # Largura do tabuleiro
        self.altura_tab = 600   # Altura do tabuleiro
        # Calcula a posição do topo e da esquerda para centralizar o tabuleiro
        self.topo = (ALTURA_JANELA - self.altura_tab) // 2
        self.esquerda = (LARGURA_JANELA - self.largura_tab) // 2
        # Define o retângulo base do tabuleiro
        self.base_tabuleiro = pygame.Rect(self.esquerda, self.topo, self.largura_tab, self.altura_tab)
        self.tamanho_celula = self.largura_tab / 3  # Tamanho de cada célula do tabuleiro
        # Fontes para exibir pontuação, modal e botões
        self.fonte_pontuacao = pygame.font.SysFont(None, 48)
        self.fonte_modal = pygame.font.SysFont(None, 72)
        self.fonte_botao = pygame.font.SysFont(None, 40)
        self.clock = pygame.time.Clock()

    def desenhar_tabuleiro(self):
        # Desenha o fundo e o tabuleiro na tela
        self.tela.fill(COR_FUNDO)
        pygame.draw.rect(self.tela, COR_TABULEIRO, self.base_tabuleiro)

        # Desenha as linhas do tabuleiro (4 linhas verticais e horizontais)
        for i in range(4):
            x_pos = self.base_tabuleiro.left + i * self.tamanho_celula
            y_pos = self.base_tabuleiro.top + i * self.tamanho_celula
            pygame.draw.line(self.tela, COR_LINHAS, (x_pos, self.base_tabuleiro.top), (x_pos, self.base_tabuleiro.bottom), 5)
            pygame.draw.line(self.tela, COR_LINHAS, (self.base_tabuleiro.left, y_pos), (self.base_tabuleiro.right, y_pos), 5)

    def desenhar_jogadas(self, tabuleiro):
        # Desenha os símbolos X e O no tabuleiro conforme o estado atual
        for linha in range(3):
            for coluna in range(3):
                centro_x = self.base_tabuleiro.left + coluna * self.tamanho_celula + self.tamanho_celula / 2
                centro_y = self.base_tabuleiro.top + linha * self.tamanho_celula + self.tamanho_celula / 2

                val = tabuleiro[linha * 3 + coluna]
                if val == 'X':
                    meia_largura_xis = 50
                    # Desenha o X com duas linhas cruzadas
                    pygame.draw.line(self.tela, COR_X,
                                     (centro_x - meia_largura_xis, centro_y - meia_largura_xis),
                                     (centro_x + meia_largura_xis, centro_y + meia_largura_xis), 15)
                    pygame.draw.line(self.tela, COR_X,
                                     (centro_x + meia_largura_xis, centro_y - meia_largura_xis),
                                     (centro_x - meia_largura_xis, centro_y + meia_largura_xis), 15)
                elif val == 'O':
                    # Desenha o O como um círculo
                    pygame.draw.circle(self.tela, COR_O, (int(centro_x), int(centro_y)), 60, 10)

    def exibir_pontuacao(self, p1, p2, empates, tempo_medio_ia1=0.0, tempo_medio_ia2=0.0):
        # Exibe a pontuação dos jogadores e empates na lateral do tabuleiro
        fonte = pygame.font.SysFont(None, 18)
        margem = 10
        altura_linha = 20
        x = self.base_tabuleiro.right + margem
        y = self.base_tabuleiro.top

        texto_p1 = fonte.render(f"Jogador 1: {p1}", True, COR_TEXTO)
        texto_p2 = fonte.render(f"Jogador 2: {p2}", True, COR_TEXTO)
        texto_empate = fonte.render(f"Empates: {empates}", True, COR_TEXTO)
        texto_tempo_ia1 = fonte.render(f"Tempo médio IA 1: {tempo_medio_ia1:.4f}s", True, COR_TEXTO)
        texto_tempo_ia2 = fonte.render(f"Tempo médio IA 2: {tempo_medio_ia2:.4f}s", True, COR_TEXTO)

        # Desenha os textos na tela
        self.tela.blit(texto_p1, (x, y))
        self.tela.blit(texto_p2, (x, y + altura_linha))
        self.tela.blit(texto_empate, (x, y + 2 * altura_linha))
        self.tela.blit(texto_tempo_ia1, (x, y + 3 * altura_linha))
        self.tela.blit(texto_tempo_ia2, (x, y + 4 * altura_linha))

    def botao_pause(self, pausado):
        fonte = self.fonte_botao
        margem = 10
        altura_linha = 20
        x_pause = self.base_tabuleiro.right + margem
        y_pause = self.base_tabuleiro.top + 6 * altura_linha

        texto = "Continuar" if pausado else "Pausar"
        texto_pause = fonte.render(texto, True, COR_BOTAO_TEXTO)

        largura_botao = 150
        altura_botao = 50

        botao_pause_rect = pygame.Rect(x_pause, y_pause, largura_botao, altura_botao)
        pygame.draw.rect(self.tela, COR_BOTAO_JOGAR, botao_pause_rect, border_radius=10)
        self.tela.blit(texto_pause, (
            x_pause + (largura_botao - texto_pause.get_width()) // 2,
            y_pause + (altura_botao - texto_pause.get_height()) // 2
        ))

        return botao_pause_rect
    
    def tela_pausado(self):
        largura_modal = 400
        altura_modal = 200
        x_modal = (LARGURA_JANELA - largura_modal) // 2
        y_modal = (ALTURA_JANELA - altura_modal) // 2

        botao_continuar = pygame.Rect(x_modal + 75, y_modal + 100, 250, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if botao_continuar.collidepoint(event.pos):
                        return  # Sai da pausa

            pygame.display.flip()
            self.clock.tick(60)

    def exibir_status_pausa(self):
        texto = self.fonte_botao.render("PAUSADO", True, COR_TEXTO)
        self.tela.blit(texto, (20, 20))  # Canto superior esquerdo

    def exibir_vencedor(self, vencedor, tabuleiro=None, p1=0, p2=0, empates=0):
        # Exibe a tela modal com o resultado da partida (vencedor ou empate)
        if vencedor == 0:
            texto_vencedor = self.fonte_modal.render('Empate!', True, COR_TEXTO)
        else:
            texto_vencedor = self.fonte_modal.render(f'Jogador {vencedor} venceu!', True, COR_TEXTO)

        # Define dimensões e posição do modal
        largura_modal = 500
        altura_modal = 320
        x_modal = (LARGURA_JANELA - largura_modal) // 2
        y_modal = (ALTURA_JANELA - altura_modal) // 2
        modal_rect = pygame.Rect(x_modal, y_modal, largura_modal, altura_modal)

        # Define botões "Jogar Novamente" e "Sair"
        largura_botao = 250
        altura_botao = 60
        x_botao_jogar_novamente = (LARGURA_JANELA - largura_botao) // 2
        y_botao_jogar_novamente = (ALTURA_JANELA - altura_botao) // 2
        botao_jogar_novamente = pygame.Rect(x_botao_jogar_novamente, y_botao_jogar_novamente, largura_botao, altura_botao)

        x_botao_sair = (LARGURA_JANELA - largura_botao) // 2
        y_botao_sair = (ALTURA_JANELA - altura_botao + 170) // 2
        botao_sair = pygame.Rect(x_botao_sair, y_botao_sair, largura_botao, altura_botao)

        # Loop para exibir o modal e tratar eventos de clique nos botões
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if botao_jogar_novamente.collidepoint(event.pos):
                        return False  # Indica reinício do jogo
                    elif botao_sair.collidepoint(event.pos):
                        pygame.quit()
                        exit()

            # Desenha o tabuleiro por trás do modal
            self.desenhar_tabuleiro()
            if tabuleiro is not None:
                self.desenhar_jogadas(tabuleiro)
            else:
                self.desenhar_jogadas([0]*9)
            self.exibir_pontuacao(p1, p2, empates)

            # Desenha o modal com fundo e borda arredondada
            pygame.draw.rect(self.tela, COR_MODAL_FUNDO, modal_rect, border_radius=20)
            pygame.draw.rect(self.tela, COR_MODAL_BORDA, modal_rect, width=5, border_radius=20)

            # Exibe o texto do vencedor no modal
            self.tela.blit(texto_vencedor, (
                x_modal + (largura_modal - texto_vencedor.get_width()) // 2,
                y_modal + 40
            ))

            # Fonte para os botões
            fonte_botao = pygame.font.SysFont(None, 40)

            # Desenha o botão "Jogar Novamente"
            pygame.draw.rect(self.tela, COR_BOTAO_JOGAR, botao_jogar_novamente, border_radius=10)
            texto_jogar = fonte_botao.render("Jogar Novamente", True, COR_BOTAO_TEXTO)
            self.tela.blit(texto_jogar, (
                botao_jogar_novamente.x + (largura_botao - texto_jogar.get_width()) // 2,
                botao_jogar_novamente.y + (altura_botao - texto_jogar.get_height()) // 2
            ))

            # Desenha o botão "Sair"
            pygame.draw.rect(self.tela, COR_BOTAO_SAIR, botao_sair, border_radius=10)
            texto_sair = fonte_botao.render("Sair", True, COR_BOTAO_TEXTO)
            self.tela.blit(texto_sair, (
                botao_sair.x + (largura_botao - texto_sair.get_width()) // 2,
                botao_sair.y + (altura_botao - texto_sair.get_height()) // 2
            ))

            pygame.display.flip()
            self.clock.tick(60)
