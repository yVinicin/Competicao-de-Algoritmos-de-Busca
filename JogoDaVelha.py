# Alunos:
#   Equipe 1: Gabriel Pereira e Gabriel Neneve
#   Equipe 2: Thalita e Vinícius Mattos
# Disciplina: Inteligência Artificial - Profª Adriana Postal
# Problema: Jogo da Velha - Competição de Algoritmos
# Algoritmos: Minimax com Tabela de Transposição (MTT) e Alpha-Beta Pruning

class JogoDaVelha:
    def __init__(self):
        # Inicializa o tabuleiro com 9 espaços vazios e sem vencedor
        self.tabuleiro = [' ' for _ in range(9)]  # Lista 9 posições: 'X', 'O' ou ' '
        self.vencedor_atual = None

    def fazer_jogada(self, posicao, letra):
        # Realiza uma jogada na posição especificada com a letra ('X' ou 'O')
        if self.tabuleiro[posicao] == ' ':
            self.tabuleiro[posicao] = letra
            # Verifica se essa jogada resultou em vitória
            if self.checar_vencedor(posicao, letra):
                self.vencedor_atual = letra
            return True
        return False

    def checar_vencedor(self, posicao, letra):
        # Verifica se o jogador com a letra venceu após a jogada na posição
        linha = posicao // 3
        linha_completa = self.tabuleiro[linha*3:(linha+1)*3]
        if all(spot == letra for spot in linha_completa):
            return True

        coluna = posicao % 3
        coluna_completa = [self.tabuleiro[coluna + i*3] for i in range(3)]
        if all(spot == letra for spot in coluna_completa):
            return True

        if posicao % 2 == 0:  # Possível diagonal
            diagonal1 = [self.tabuleiro[i] for i in [0,4,8]]
            if all(spot == letra for spot in diagonal1):
                return True
            diagonal2 = [self.tabuleiro[i] for i in [2,4,6]]
            if all(spot == letra for spot in diagonal2):
                return True

        return False

    def tem_espaco_vazio(self):
        # Verifica se ainda há espaços vazios no tabuleiro
        return ' ' in self.tabuleiro

    def jogadas_disponiveis(self):
        # Retorna uma lista das posições disponíveis para jogada
        return [i for i, spot in enumerate(self.tabuleiro) if spot == ' ']

    def resetar(self):
        # Reseta o tabuleiro e o vencedor atual para iniciar novo jogo
        self.tabuleiro = [' ' for _ in range(9)]
        self.vencedor_atual = None

    def desfazer_jogada(self, posicao):
        # Desfaz a jogada na posição especificada
        if self.tabuleiro[posicao] != ' ':
            self.tabuleiro[posicao] = ' '
            # Recalcula o vencedor atual após desfazer a jogada
            self.vencedor_atual = None
            for i, letra in enumerate(self.tabuleiro):
                if letra != ' ' and self.checar_vencedor(i, letra):
                    self.vencedor_atual = letra
                    break
