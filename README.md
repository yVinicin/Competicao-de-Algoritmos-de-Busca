# 🤖 Competição de Algoritmos de Busca

> Implementação de algoritmos de busca competitiva aplicados ao jogo da velha (Tic-Tac-Toe), desenvolvido para a disciplina de Inteligência Artificial.

![Badge Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)
![Badge AI](https://img.shields.io/badge/Topic-Artificial%20Intelligence-orange?logo=openai&logoColor=white)
![Badge Academic](https://img.shields.io/badge/Type-Academic%20Project-blue)

## 🏫 Sobre o Projeto

Este projeto foi desenvolvido como o 1º Trabalho da disciplina de **Inteligência Artificial** da **Universidade Estadual do Oeste do Paraná (Unioeste)**.

O objetivo é criar uma interface gráfica para o Jogo da Velha e implementar agentes inteligentes que utilizam algoritmos de busca para competir entre si ou contra um jogador humano. O foco é analisar o desempenho e a tomada de decisão de diferentes estratégias de IA.

## 📂 Estrutura do Projeto

Os códigos fonte estão organizados dentro da pasta `src`:

```bash
Competicao-de-Algoritmos-de-Busca/
├── src/
│   ├── Interface.py         # Gerenciamento da interface gráfica (GUI)
│   ├── JogadorIA.py         # Implementação dos agentes inteligentes (Algoritmos)
│   ├── JogoDaVelha.py       # Lógica principal do jogo (regras, tabuleiro)
│   └── main.py              # Arquivo principal para execução
├── Relatório...pdf          # Análise dos resultados obtidos
├── TrabalhoBusca2025.pdf    # Enunciado do trabalho
└── README.md                # Documentação
```

## 🚀 Como Executar

Certifique-se de ter o **Python 3** instalado em sua máquina.

### Passo a passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/yVinicin/Competicao-de-Algoritmos-de-Busca.git](https://github.com/yVinicin/Competicao-de-Algoritmos-de-Busca.git)
    cd Competicao-de-Algoritmos-de-Busca
    ```

2.  **Execute o jogo:**
    Como os arquivos estão em `src`, você deve navegar até lá ou executar referenciando o caminho.
    * **Linux/Mac:**
        ```bash
        python3 src/main.py
        ```
    * **Windows:**
        ```bash
        python src/main.py
        ```

3.  **Interaja:**
    A interface gráfica abrirá, permitindo que você selecione os modos de jogo (Humano vs IA, IA vs IA) e visualize as partidas.

## 🧠 Algoritmos e Conceitos

O projeto explora conceitos fundamentais de IA para jogos de soma zero, como:
* **Espaço de Estados:** Representação de todas as jogadas possíveis.
* **Função de Utilidade:** Avaliação de quão bom é um estado (vitória, derrota ou empate).
* **Algoritmos de Busca:** Busca competitiva para determinar a melhor jogada.
